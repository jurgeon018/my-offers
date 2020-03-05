import copy
from datetime import datetime
from typing import Optional

import asyncpgsa
import pytz
from sqlalchemy.dialects.postgresql import insert

from my_offers import entities, pg
from my_offers.entities.get_offers import OfferCounters
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


async def get_offer_counters(user_id: int) -> OfferCounters:
    query = """
        select
            status_tab,
            count(*) as cnt
        from
            offers
        where
            master_user_id = $1
        group by
            status_tab
    """

    rows = await pg.get().fetch(query, user_id)
    counters = {row['status_tab']: row['cnt'] for row in rows}

    return OfferCounters(
        active=counters.get('active', 0),
        not_active=counters.get('not_active', 0),
        declined=counters.get('declined', 0),
        archived=counters.get('archived'),
    )
