from typing import List, Dict

import asyncpgsa
from sqlalchemy.dialects.postgresql import insert

from my_offers import entities, pg
from my_offers.mappers.offer_import_error_mapper import offer_import_error_mapper
from my_offers.repositories.postgresql import tables


TABLE = tables.offers_last_import_error.c


async def upsert_offer_import_errors(errors: List[entities.OfferImportError]) -> None:
    data = [offer_import_error_mapper.map_to(error) for error in errors]

    insert_query = insert(tables.offers_last_import_error)

    query, params = asyncpgsa.compile_query(
        insert_query
        .values(data)
        .on_conflict_do_update(
            index_elements=[TABLE.offer_id],
            where=TABLE.created_at < insert_query.excluded.created_at,
            set_={
                'type': insert_query.excluded.type,
                'message': insert_query.excluded.message,
                'created_at': insert_query.excluded.created_at,
            }
        )
    )

    await pg.get().execute(query, *params)


async def delete_offer_import_error(offer_id: int) -> None:
    query = 'DELETE FROM my_offers.public.offers_last_import_error WHERE offer_id = $1'

    await pg.get().execute(query, offer_id)


async def get_last_import_errors(offer_ids: List[int]) -> Dict[int, str]:
    query = """
        SELECT
            offer_id,
            message
        FROM
            offers_last_import_error
        WHERE
            offer_id = ANY($1::BIGINT[])
    """

    rows = await pg.get().fetch(query, offer_ids)
    if not rows:
        return {}

    return {row['offer_id']: row['message'] for row in rows}
