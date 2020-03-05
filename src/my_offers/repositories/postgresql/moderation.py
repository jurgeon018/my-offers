from typing import List

import asyncpgsa
from sqlalchemy.dialects.postgresql import insert

from my_offers import pg
from my_offers.entities.moderation import OfferOffence
from my_offers.enums import ModerationOffenceStatus
from my_offers.mappers.moderation import offer_offence_mapper
from my_offers.repositories.postgresql.tables import offers_offences


async def save_offer_offence(offer_offence: OfferOffence) -> None:
    insert_values = offer_offence_mapper.map_to(offer_offence)

    # меняем только дату обновления для update
    update_values = insert_values.copy()
    update_values.pop('created_at', None)

    query, params = asyncpgsa.compile_query(
        insert(
            offers_offences
        ).values([
            insert_values
        ]).on_conflict_do_update(
            index_elements=[offers_offences.c.offence_id],
            where=offers_offences.c.row_version < offer_offence.row_version,
            set_=update_values
        )
    )

    await pg.get().execute(query, *params)


async def get_offers_offence(*, offer_ids: List[int], status: ModerationOffenceStatus) -> List[OfferOffence]:
    sql = """
        WITH offence_ids AS (
        SELECT offence_id                                     as offence_id,
               row_number() over (order by created_date desc) as row_number
        from offers_offences
        WHERE offer_id = ANY ($1::bigint[])
          AND offence_status = $2
    )
        SELECT *
        FROM offers_offences oo
             JOIN offence_ids oi ON oi.offence_id = oo.offence_id AND oi.row_number = 1
    """
    params = [
        offer_ids,
        status.value
    ]
    rows = await pg.get().fetch(sql, *params)

    return [offer_offence_mapper.map_from(row) for row in rows]
