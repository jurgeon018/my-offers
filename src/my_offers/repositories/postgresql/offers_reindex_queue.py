from typing import List

from my_offers import pg
from my_offers.entities import ReindexOfferItem
from my_offers.mappers.offer_mapper import reindex_offer_item_mapper


async def get_reindex_items(limit: int = 100) -> List[ReindexOfferItem]:
    query = """
    with offer_ids as (
        select
            offer_id
        from
            offers_reindex_queue
        where
            not in_process
        order by
            created_at
        limit $1
        for update
    )
    update
        offers_reindex_queue
    set
        in_process = true
    from
        offer_ids
    where
        offers_reindex_queue.offer_id = offer_ids.offer_id
    returning
        offers_reindex_queue.offer_id, sync, created_at
    """

    rows = await pg.get().fetch(query, limit)

    return [reindex_offer_item_mapper.map_from(row) for row in rows]


async def delete_reindex_items(offer_ids: List[int]) -> None:
    query = 'DELETE FROM offers_reindex_queue WHERE offer_id = ANY($1::BIGINT[])'
    await pg.get().execute(query, offer_ids)
