import asyncio
import logging

from simple_settings import settings

from my_offers.repositories.postgresql.offer import update_offers_master_user_id_and_payed_by
from my_offers.repositories.postgresql.offers_reindex_queue import delete_reindex_items, get_reindex_items


logger = logging.getLogger(__name__)


async def reindex_offers_master_and_payed_by_command() -> None:
    cnt = 0
    while reindex_items := await get_reindex_items(settings.REINDEX_CHUNK):
        logger.info('Selected %s offers', len(reindex_items))
        offer_ids = [item.offer_id for item in reindex_items]
        await update_offers_master_user_id_and_payed_by(offer_ids)
        await delete_reindex_items(offer_ids)

        cnt += len(reindex_items)
        logger.info('Processed %s offers', cnt)

        await asyncio.sleep(settings.REINDEX_TIMEOUT)
