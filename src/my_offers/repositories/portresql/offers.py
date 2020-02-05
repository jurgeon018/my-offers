import copy
from dataclasses import asdict
from datetime import datetime

import asyncpgsa
import pytz
from sqlalchemy.dialects.postgresql import insert

from my_offers import entities, pg
from my_offers.mappers.offer_mapper import offer_mapper
from my_offers.repositories.portresql import tables


ENUM_FIELDS = ('deal_type', 'offer_type', 'status_tab')


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
            where=(tables.offers.c.row_version < offer.row_version),
            set_=update
        )
    )

    await pg.get().fetch(query, *params)
