from datetime import datetime
from typing import List

import sqlalchemy as sa

from my_offers import pg
from my_offers.repositories.postgresql.tables import metadata


offers_delete_queue = sa.Table(
    'offers_delete_queue',
    metadata,
    sa.Column('offer_id', sa.BIGINT, primary_key=True),
    sa.Column('created_at', sa.TIMESTAMP, nullable=False),
    sa.Column('delete_at', sa.TIMESTAMP, nullable=False),
)


async def get_offer_ids_for_delete(limit: int, timeout: int) -> List[int]:
    query = 'select offer_id from offers_delete_queue where delete_at < current_timestamp order by delete_at limit $1'

    rows = await pg.get().fetch(query, limit, timeout=timeout)

    return [row['offer_id'] for row in rows]


async def add_offer_to_delete_queue(offer_id: int, delete_at: datetime) -> None:
    query = 'insert into offers_delete_queue(offer_id, delete_at) values($1, $2) on conflict do nothing'

    await pg.get().execute(query, offer_id, delete_at)
