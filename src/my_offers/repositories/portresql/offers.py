from dataclasses import asdict
from datetime import datetime
from typing import List

import asyncpgsa
import pytz
from sqlalchemy import and_, select
from sqlalchemy.dialects.postgresql import insert

from my_offers import entities, pg
from my_offers.enums import OfferStatusTab
from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel
from my_offers.repositories.portresql import tables
from my_offers.schemas.object_model import ObjectModelSchema


ENUM_FIELDS = ('deal_type', 'offer_type', 'status_tab')


async def save_offer(offer: entities.Offer) -> None:
    now = datetime.now(tz=pytz.UTC)
    values = asdict(offer)
    for field in ENUM_FIELDS:
        values[field] = values[field].name

    values['services'] = [service.name for service in offer.services]
    values['created_at'] = now
    values['updated_at'] = now
    # TODO: переделать на маппер

    query, params = asyncpgsa.compile_query(
        insert(tables.offers)
            .values([values])
            .on_conflict_do_nothing()
    )

    await pg.get().fetch(query, *params)


async def get_offers_by_status(
        *,
        status_tab: OfferStatusTab,
        user_id: int
) -> List[ObjectModel]:
    sql = (
        select([
            tables.offers.c.raw_data,
        ])
        .where(and_(
            tables.offers.c.status_tab == status_tab.value,
            tables.offers.c.master_user_id == user_id
        ))
        .limit(20)
    )

    query, params = asyncpgsa.compile_query(sql)
    result = await pg.get().fetch(query, *params)

    return [
        ObjectModelSchema().loads(r['raw_data']).data  # TODO: check errors
        for r in result
    ]
