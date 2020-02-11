import copy
from datetime import datetime
from typing import List

import asyncpgsa
import pytz
from cian_json import json
from sqlalchemy import and_, select
from sqlalchemy.dialects.postgresql import insert

from my_offers import entities, pg
from my_offers.enums import GetOfferStatusTab
from my_offers.mappers.object_model import object_model_mapper
from my_offers.mappers.offer_mapper import offer_mapper
from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel
from my_offers.repositories.postgresql import tables


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
        status_tab: GetOfferStatusTab,
        user_id: int,
        limit: int = 20
) -> List[ObjectModel]:
    sql = (
        select([
            tables.offers.c.raw_data,
        ])
        .where(and_(
            tables.offers.c.status_tab == status_tab.value,
            tables.offers.c.master_user_id == user_id
        ))
        .limit(limit)
    )

    query, params = asyncpgsa.compile_query(sql)
    result = await pg.get().fetch(query, *params)

    return [
        object_model_mapper.map_from(json.loads(r['raw_data']))
        for r in result
    ]
