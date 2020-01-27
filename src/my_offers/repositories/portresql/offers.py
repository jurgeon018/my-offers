from dataclasses import asdict
from datetime import datetime

import asyncpgsa
import pytz
from my_offers import entities, pg
from my_offers.repositories.portresql import tables
from sqlalchemy.dialects.postgresql import insert


async def save_offer(offer: entities.Offer) -> None:
    now = datetime.now(tz=pytz.UTC)
    values = asdict(offer)
    values['deal_type'] = offer.deal_type.name
    values['offer_type'] = offer.offer_type.name
    values['status'] = offer.status.name
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
