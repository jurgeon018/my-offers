from typing import List

import asyncpgsa
import sqlalchemy as sa
from sqlalchemy import delete

from my_offers import pg


async def delete_rows_by_offer_id(table: sa.Table, offer_ids: List[int], timeout: int) -> None:

    query, params = asyncpgsa.compile_query(
        delete(table)
        .where(
            table.c.offer_id.in_(offer_ids),
        )
    )
    await pg.get().execute(query, *params, timeout=timeout)
