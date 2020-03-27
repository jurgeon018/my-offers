from datetime import datetime
from typing import List

import asyncpgsa
import pytz
from sqlalchemy.dialects.postgresql import insert

from my_offers import pg
from my_offers.entities.moderation import OfferPremoderation
from my_offers.mappers.moderation import offer_premoderation_mapper
from my_offers.repositories.postgresql import tables


async def save_offer_premoderation(offer_premoderation: OfferPremoderation) -> None:
    values = offer_premoderation_mapper.map_to(offer_premoderation)
    now = datetime.now(tz=pytz.UTC)
    values['created_at'] = now

    insert_query = insert(tables.offers_premoderations)

    query, params = asyncpgsa.compile_query(
        insert_query
        .values(values)
        .on_conflict_do_update(
            index_elements=[tables.offers_premoderations.c.offer_id],
            where=tables.offers_premoderations.c.row_version < insert_query.excluded.row_version,
            set_={
                'removed': insert_query.excluded.removed,
                'row_version': insert_query.excluded.row_version,
                'updated_at': now,
            }
        )
    )

    await pg.get().execute(query, *params)


async def get_offer_premoderations(offer_ids: List[int]) -> List[int]:
    query = 'SELECT offer_id FROM offers_premoderations WHERE offer_id = ANY($1::BIGINT[]) AND NOT removed'

    rows = await pg.get().fetch(query, offer_ids)

    return [row['offer_id'] for row in rows]
