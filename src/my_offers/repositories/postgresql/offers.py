import copy
from datetime import datetime
from typing import List, Dict, Any

import asyncpgsa
import pytz
from cian_json import json
from sqlalchemy import and_, select, func
from sqlalchemy.dialects.postgresql import insert

from my_offers import entities, pg
from my_offers.mappers.object_model import object_model_mapper
from my_offers.mappers.offer_mapper import offer_mapper
from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel
from my_offers.repositories.postgresql import tables


OFFER_TABLE = tables.offers.c

FILTERS_MAP = {
    'status_tab': OFFER_TABLE.status_tab,
    'deal_type': OFFER_TABLE.deal_type,
    'offer_type': OFFER_TABLE.offer_type,
    'has_photo': OFFER_TABLE.has_photo,
    'is_manual': OFFER_TABLE.is_manual,
    'is_in_hidden_base': OFFER_TABLE.is_in_hidden_base,
}


async def save_offer(offer: entities.Offer) -> None:
    values = offer_mapper.map_to(offer)

    now = datetime.now(tz=pytz.UTC)
    values['updated_at'] = now

    update = copy.deepcopy(values)
    del update['offer_id']

    values['created_at'] = now

    query, params = asyncpgsa.compile_query(
        insert(tables.offers)
        .values([values])
        .on_conflict_do_update(
            index_elements=[tables.offers.c.offer_id],
            where=tables.offers.c.row_version < offer.row_version,
            set_=update
        )
    )

    await pg.get().execute(query, *params)


async def get_object_models(
        *,
        filters: Dict[str, Any],
        master_user_id: int,
        limit: int = 20
) -> List[ObjectModel]:
    # todo: незабыть про newobjects
    conditions = [OFFER_TABLE.master_user_id == master_user_id]
    if services := filters['services']:
        conditions.append(OFFER_TABLE.services.any_(services).all_())
    if sub_agent_ids := filters['sub_agent_ids']:
        conditions.append(OFFER_TABLE.sub_agent_ids.any_(sub_agent_ids).all_())
    if search_text := filters['search_text']:
        conditions.append(
            func.to_tsvector('russian', OFFER_TABLE.search_text).match(search_text, postgresql_regconfig='russian')
        )

    for key, value in filters.items():
        if key not in FILTERS_MAP:
            continue
        if value is None:
            continue
        conditions.append(FILTERS_MAP[key] == value)

    sql = (
        select([OFFER_TABLE.raw_data])
        .where(and_(*conditions))
        .order_by(OFFER_TABLE.sort_date.desc().nullslast(), OFFER_TABLE.offer_id)
        .limit(limit)
    )

    query, params = asyncpgsa.compile_query(sql)
    result = await pg.get().fetch(query, *params)

    return [
        object_model_mapper.map_from(json.loads(r['raw_data']))
        for r in result
    ]
