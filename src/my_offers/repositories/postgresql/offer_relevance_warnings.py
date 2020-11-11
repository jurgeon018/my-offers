from typing import List

import asyncpgsa
from sqlalchemy.dialects.postgresql import insert

from my_offers import pg
from my_offers.entities import OfferRelevanceWarning
from my_offers.mappers.offer_relevance_warning_mapper import offer_relevance_warning_mapper
from my_offers.repositories.postgresql.tables import offer_relevance_warnings


async def get_offer_relevance_warnings(offer_ids: List[int]) -> List[OfferRelevanceWarning]:
    query = """
    SELECT
        offer_id,
        check_id,
        created_at,
        updated_at,
        due_date,
        finished
    FROM
        offer_relevance_warnings
    WHERE
        offer_id = ANY($1::BIGINT[]) AND
        finished IS NOT TRUE
    """

    rows = await pg.get().fetch(query, offer_ids)

    return [offer_relevance_warning_mapper.map_from(row) for row in rows]


async def save_offer_relevance_warning(offer_relevance_warning: OfferRelevanceWarning) -> None:
    insert_values = offer_relevance_warning_mapper.map_to(offer_relevance_warning)
    insert_query = insert(offer_relevance_warnings)

    query, params = asyncpgsa.compile_query(
        insert_query.values(
            [insert_values]
        ).on_conflict_do_update(
            index_elements=[offer_relevance_warnings.c.offer_id],
            set_={
                'check_id': insert_query.excluded.check_id,
                'updated_at': insert_query.excluded.updated_at,
                'due_date': insert_query.excluded.due_date,
                'finished': insert_query.excluded.finished,
            }
        )
    )

    await pg.get().execute(query, *params)
