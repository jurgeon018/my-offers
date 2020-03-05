import copy
from datetime import datetime
from typing import Optional

import asyncpgsa
import pytz
from simple_settings import settings
from sqlalchemy.dialects.postgresql import insert

from my_offers import entities, enums, pg
from my_offers.mappers.offer_mapper import offer_mapper
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


async def get_offer_by_id(offer_id: int) -> Optional[entities.Offer]:
    query = 'SELECT * FROM offers WHERE offer_id = $1'

    row = await pg.get().fetchrow(query, offer_id)

    if not row:
        return None

    return offer_mapper.map_from(row)


async def delete_offers_older_than(days_count: int = settings.COUNT_DAYS_HOLD_DELETED_OFFERS):
    query = """DELETE FROM offers where status_tab = $1 and updated_at <= now() - $2 * interval  '1 day'"""

    await pg.get().execute(
        query,
        enums.OfferStatusTab.deleted.name,
        days_count
    )
