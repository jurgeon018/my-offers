from typing import List, Optional

import asyncpgsa
from sqlalchemy import and_, desc, select
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
    sql = (
        select([
            offers_offences
        ]).where(and_(
            offers_offences.c.offer_id.in_(offer_ids),
            offers_offences.c.offence_status == status.value,
        )).order_by(
            desc(offers_offences.c.created_date)
        )
    )
    query, params = asyncpgsa.compile_query(sql)
    rows = await pg.get().fetchrow(query, *params)

    return [offer_offence_mapper.map_from(row) for row in rows]
