from datetime import datetime

import asyncpgsa
import pytz
from sqlalchemy.dialects.postgresql import insert

from my_offers import pg
from my_offers.repositories.postgresql import tables


async def save_last_visit_date(user_id: int) -> None:
    insert_query = insert(tables.moderation_alerts)

    values = dict(
        user_id=user_id,
        last_visit_date=datetime.now(tz=pytz.UTC),
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
