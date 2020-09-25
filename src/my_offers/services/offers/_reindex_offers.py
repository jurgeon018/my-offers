import asyncio
import json
import logging
from typing import List, Tuple

from simple_settings import settings

from my_offers.entities import ReindexOffer
from my_offers.mappers.object_model import object_model_mapper
from my_offers.repositories.monolith_cian_elasticapi import get_api_elastic_announcement_get
from my_offers.repositories.monolith_cian_elasticapi.entities import (
    ElasticResultIElasticAnnouncementElasticAnnouncementError,
    GetApiElasticAnnouncementGet,
)
from my_offers.repositories.postgresql.offer import get_offers_for_reindex, set_offers_is_deleted
from my_offers.repositories.postgresql.offers_reindex_queue import delete_reindex_items, get_reindex_items
from my_offers.services.announcement import process_announcement_service
from my_offers.services.realty_resender._jobs import ELASTIC_OFFER_INVALID_CODES


logger = logging.getLogger(__name__)


async def reindex_offers_command() -> None:
    cnt = 0
    while reindex_items := await get_reindex_items():
        logger.info('Selected %s offers', len(reindex_items))
        offer_ids_map = {}
        offer_ids = []
        offer_for_sync_ids = []
        for reindex_item in reindex_items:
            offer_ids_map[reindex_item.offer_id] = reindex_item.created_at
            if reindex_item.sync:
                offer_for_sync_ids.append(reindex_item.offer_id)
            else:
                offer_ids.append(reindex_item.offer_id)

        offers, not_found_ids = await load_offers(offer_ids=offer_ids, offer_for_sync_ids=offer_for_sync_ids)

        for reindex_offer in offers:
            if reindex_offer.updated_at and reindex_offer.updated_at > offer_ids_map[reindex_offer.offer_id]:
                continue

            object_model = object_model_mapper.map_from(json.loads(reindex_offer.raw_data))
            processor = process_announcement_service.ForceAnnouncementProcessor()
            await processor.process(object_model)

        if not_found_ids:
            await set_offers_is_deleted(not_found_ids)

        await delete_reindex_items(list(offer_ids_map.keys()))

        cnt += len(reindex_items)
        logger.info('Processed %s offers', cnt)


async def load_offers(*, offer_ids: List[int], offer_for_sync_ids: List[int]) -> Tuple[List[ReindexOffer], List[int]]:
    result: List[ReindexOffer] = []
    not_found_ids: List[int] = []

    if offer_ids:
        result.extend(await get_offers_for_reindex(offer_ids))

    if offer_for_sync_ids:
        reindex_offers, not_found_ids = await get_offers_from_elasticapi_for_reindex(offer_for_sync_ids)
        result.extend(reindex_offers)

    return result, not_found_ids


async def get_offers_from_elasticapi_for_reindex(offer_ids: List[int]) -> Tuple[List[ReindexOffer], List[int]]:
    result = []
    not_found_ids = []
    chunk_size = settings.ELASTIC_API_BULK_SIZE
    for i in range(0, len(offer_ids), chunk_size):
        if i:
            await asyncio.sleep(settings.ELASTIC_API_DELAY)

        response: ElasticResultIElasticAnnouncementElasticAnnouncementError = await get_api_elastic_announcement_get(
            GetApiElasticAnnouncementGet(ids=offer_ids[i: i + chunk_size])
        )

        if response.success:
            for item in response.success:
                result.append(ReindexOffer(
                    offer_id=item.realty_object_id,
                    raw_data=item.object_model,
                ))

        if response.errors:
            for error in response.errors:
                if error.code in ELASTIC_OFFER_INVALID_CODES:
                    not_found_ids.append(error.realty_object_id)
                else:
                    logger.error('Sync offer %s error: %s', error.realty_object_id, error.message)

    return result, not_found_ids
