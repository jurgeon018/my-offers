from dataclasses import asdict
from datetime import datetime

import asyncpgsa
import pytz
from sqlalchemy.dialects.postgresql import insert

from my_offers import entities, pg
from my_offers.repositories.portresql import tables


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
