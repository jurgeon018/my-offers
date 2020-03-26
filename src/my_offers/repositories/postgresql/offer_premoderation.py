from datetime import datetime

import asyncpgsa
import pytz
from sqlalchemy.dialects.postgresql import insert

from my_offers import pg
from my_offers.entities.moderation import OfferPremoderation
from my_offers.mappers.moderation import offer_premoderation_mapper
from my_offers.repositories.postgresql import tables


async def save_offer_premoderation(offer_premoderation: OfferPremoderation) -> None:
    values = offer_premoderation_mapper.map_from(offer_premoderation)
    now = datetime.now(tz=pytz.UTC)
    values['created_at'] = now

    insert_query = insert(tables.offer_premoderation)

    query, params = asyncpgsa.compile_query(
        insert_query
        .values(values)
        .on_conflict_do_update(
            index_elements=[tables.offer_premoderation.c.offer_id],
            where=tables.offer_premoderation.c.row_version < insert_query.excluded.row_version,
            set_={
                'removed': insert_query.excluded.removed,
                'row_version': insert_query.excluded.row_version,
                'updated_at': now,
            }
        )
    )

    await pg.get().execute(query, *params)
