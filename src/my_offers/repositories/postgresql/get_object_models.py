from typing import Any, Dict, List

import asyncpgsa
import sqlalchemy as sa
from cian_json import json
from sqlalchemy import and_, any_, cast, func, select

from my_offers import pg
from my_offers.mappers.object_model import object_model_mapper
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
    'master_user_id': OFFER_TABLE.master_user_id,
    'sub_agent_ids': OFFER_TABLE.user_id,
}


async def get_object_models(
        *,
        filters: Dict[str, Any],
        limit: int,
        offset: int,
) -> List[ObjectModel]:
    conditions = _prepare_conditions(filters)
    sort = [OFFER_TABLE.sort_date.desc().nullslast(), OFFER_TABLE.offer_id]

    sql = (
        select([OFFER_TABLE.raw_data])
        .where(and_(*conditions))
        .order_by(*sort)
        .limit(limit)
        .offset(offset)
    )

    query, params = asyncpgsa.compile_query(sql)
    result = await pg.get().fetch(query, *params)

    return [
        object_model_mapper.map_from(json.loads(r['raw_data']))
        for r in result
    ]


def _prepare_conditions(filters: Dict[str, Any],):
    conditions = []
    for key, value in filters.items():
        if key not in FILTERS_MAP:
            continue
        if value is None:
            continue
        field = FILTERS_MAP[key]
        if isinstance(value, list):
            conditions.append(field == any_(cast(value, sa.ARRAY(field.type))))
        else:
            conditions.append(field == value)

    if services := filters.get('services'):
        conditions.append(OFFER_TABLE.services.contains(services))
    if search_text := filters.get('search_text'):
        conditions.append(
            func.to_tsvector('russian', OFFER_TABLE.search_text).match(search_text, postgresql_regconfig='russian')
        )

    return conditions
