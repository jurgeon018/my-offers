from datetime import datetime
from typing import List

import asyncpgsa
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import insert

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


async def add_offer_to_delete_queue(offer_ids: List[int], delete_at: datetime) -> None:
    data = [{'offer_id': offer_id, 'delete_at': delete_at} for offer_id in set(offer_ids)]

    insert_query = insert(offers_delete_queue)
    query, params = asyncpgsa.compile_query(
        insert_query
        .values(data)
        .on_conflict_do_nothing()
    )

    await pg.get().execute(query, *params)


async def add_offer_to_delete_queue_by_master_user_id(user_id: int) -> None:
    query = """
    insert into offers_delete_queue(offer_id, delete_at)
    select
        offer_id,
        current_timestamp
    from
        offers
    where
        master_user_id = $1
    on conflict do nothing
    """

    await pg.get().execute(query, user_id)


async def add_offer_to_delete_queue_by_user_id(*, master_user_id: int, user_id: int) -> None:
    query = """
    insert into offers_delete_queue(offer_id, delete_at)
    select
        offer_id,
        current_timestamp
    from
        offers
    where
        master_user_id = $1
        and user_id = $2
    on conflict do nothing
    """

    await pg.get().execute(query, master_user_id, user_id)
