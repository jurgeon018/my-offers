from typing import List

from my_offers import pg


async def get_reindex_items(limit: int = 100) -> List[int]:
    query = """
    with user_ids as (
        select
            user_id
        from
            users_reindex_queue
        where
            not in_process
        order by
            created_at
        limit $1
        for update
    )
    update
        users_reindex_queue
    set
        in_process = true
    from
        user_ids
    where
        users_reindex_queue.user_id = user_ids.user_id
    returning
        users_reindex_queue.user_id
    """

    rows = await pg.get().fetch(query, limit)

    return [row['id'] for row in rows]


async def delete_reindex_items(user_ids: List[int]) -> None:
    query = 'DELETE FROM users_reindex_queue WHERE user_id = ANY($1::BIGINT[])'
    await pg.get().execute(query, user_ids)
