import logging

from my_offers.repositories.monolith_cian_elasticapi import api_elastic_announcement_v3_get_changed_ids
from my_offers.repositories.monolith_cian_elasticapi.entities import ApiElasticAnnouncementV3GetChangedIds
from my_offers.repositories.postgresql import save_offer_row_versions


logger = logging.getLogger(__name__)


async def sync_offers(row_version: int = 0):
    has_next = True
    page_size = 10000
    count = 0
    while has_next:
        offer_versions = await api_elastic_announcement_v3_get_changed_ids(ApiElasticAnnouncementV3GetChangedIds(
            row_version=row_version,
            top=page_size,
        ))

        if not offer_versions:
            break

        await save_offer_row_versions(offer_versions)

        last_version = offer_versions[-1]
        row_version = last_version.row_version
        has_next = len(offer_versions) >= page_size
        count += len(offer_versions)

        logger.info('count %s  row_version %s', count, row_version)
