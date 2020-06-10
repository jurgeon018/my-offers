from datetime import datetime

from my_offers import pg


async def get_last_row_version() -> int:
    query = (
        'SELECT row_version '
        'FROM offers_resender_cron '
        'ORDER BY id DESC '
        'LIMIT 1'
    )
    row = await pg.get().fetchrow(query)

    return row['row_version']


async def save_cron_session(
        *,
        operation_id: str,
        row_version: int,
        created_at: datetime
) -> None:
    query = (
        'INSERT INTO offers_resender_cron (operation_id, row_version, created_at) '
        'VALUES ($1, $2, $3)'
    )
    params = [
        operation_id,
        row_version,
        created_at
    ]

    await pg.get().execute(query, *params)


async def save_cron_stats(
        *,
        operation_id: str,
        founded_from_elastic: int,
        need_update: int,
        not_found_in_db: int,
        created_at: datetime
):
    query = (
        'INSERT INTO offers_resender_stats '
        '(operation_id, founded_from_elastic, need_update, not_found_in_db, created_at)'
        'VALUES ($1, $2, $3, $4, $5)'
    )
    params = [
        operation_id,
        founded_from_elastic,
        need_update,
        not_found_in_db,
        created_at
    ]

    await pg.get().execute(query, *params)
