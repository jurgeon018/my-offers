from datetime import datetime
from typing import Optional

import asyncpgsa
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from my_offers import pg
from my_offers.repositories.postgresql import tables


async def save_moderation_alerts_last_visit_date(*, user_id: int, last_visit_date: datetime) -> None:
    insert_query = insert(tables.moderation_alerts)

    values = dict(
        user_id=user_id,
        last_visit_date=last_visit_date,
    )

    query, params = asyncpgsa.compile_query(
        insert_query
        .values([values])
        .on_conflict_do_update(
            index_elements=[tables.moderation_alerts.c.user_id],
            set_={
                'last_visit_date': insert_query.excluded.last_visit_date,
            }
        )
    )

    await pg.get().execute(query, *params)

    return None


async def get_last_visit_date(user_id: int) -> Optional[datetime]:
    query, params = asyncpgsa.compile_query(
        select([
            tables.moderation_alerts.c.last_visit_date,
        ]).where(
            tables.moderation_alerts.c.user_id == user_id
        )
    )

    return await pg.get().fetchval(query, *params)
