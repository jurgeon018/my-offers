import json
import logging

from my_offers.mappers.object_model import object_model_mapper
from my_offers.repositories.postgresql.offer import get_offers_for_reindex, update_offer
from my_offers.repositories.postgresql.offers_reindex_queue import delete_reindex_items, get_reindex_items
from my_offers.services.announcement.process_announcement_service import prepare_offer


logger = logging.getLogger(__name__)


async def reindex_offers_command():
    cnt = 0
    while reindex_items := await get_reindex_items():
        logger.info('Selected %s offers', len(reindex_items))
        offer_ids_map = {}
        for reindex_item in reindex_items:
            offer_ids_map[reindex_item.offer_id] = reindex_item.created_at

        offer_ids = list(offer_ids_map.keys())
        offers = await get_offers_for_reindex(offer_ids)

        for reindex_offer in offers:
            if reindex_offer.updated_at > offer_ids_map[reindex_offer.offer_id]:
                continue

            object_model = object_model_mapper.map_from(json.loads(reindex_offer.raw_data))
            offer = await prepare_offer(object_model)
            await update_offer(offer)

        await delete_reindex_items(offer_ids)

        cnt += len(reindex_items)
        logger.info('Processed %s offers', cnt)
