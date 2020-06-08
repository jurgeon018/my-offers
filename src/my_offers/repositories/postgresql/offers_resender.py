from my_offers import pg


async def get_last_row_version_for_offers() -> int:
    query = (
        'SELECT row_version '
        'FROM offers_resender_cron '
        'ORDER BY id DESC '
        'LIMIT 1'
    )
    row = await pg.get().fetchrow(query)

    return row['row_version']


async def insert_offers_stats():
    pass
