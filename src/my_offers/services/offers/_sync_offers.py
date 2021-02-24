import asyncio
import logging
from typing import List

from cian_http.exceptions import ApiClientException
from more_itertools import grouper
from simple_settings import settings

from my_offers.helpers.graphite import send_to_graphite
from my_offers.repositories.monolith_cian_ms_announcements import v2_get_changed_announcements_ids
from my_offers.repositories.monolith_cian_ms_announcements.entities import (
    GetChangedIdsV2Response,
    V2GetChangedAnnouncementsIds,
)
from my_offers.repositories.postgresql import (
    archive_missed_offers,
    clean_offer_row_versions,
    get_missed_offer_ids,
    get_offers_ids_to_archive,
    get_outdated_offer_ids,
    save_offer_row_versions,
)
from my_offers.services.realty_resender._jobs import run_resend_task


logger = logging.getLogger(__name__)


async def sync_offers(row_version: int = 0):
    # очищаем таблицу с версиями объявлений
    await clean_offer_row_versions()

    # Сходить в C# announcemens и сохранить текущие версии объявлений
    offers_count = await _save_current_offer_row_versions(row_version)
    send_to_graphite(
        key='sync_offers.total_offers_count',
        value=offers_count,
    )

    # выбираем все объявки со старыми row_version и просим С# прислать их снова
    outdated_offer_ids = await get_outdated_offer_ids()
    send_to_graphite(
        key='sync_offers.outdated_offer_ids',
        value=len(outdated_offer_ids),
    )
    await run_resend_task(outdated_offer_ids)

    # выбираем все объявки, которых у нас нет и просим С# прислать их снова
    missed_offer_ids = await get_missed_offer_ids()
    send_to_graphite(
        key='sync_offers.missed_offer_ids',
        value=len(missed_offer_ids),
    )
    await run_resend_task(missed_offer_ids)

    # выбираем все объявки, которых нет в C# и отправляем их в архив
    archived_offer_ids = await get_offers_ids_to_archive()
    send_to_graphite(
        key='sync_offers.archived_offer_ids',
        value=len(archived_offer_ids),
    )
    await _archive_offers(archived_offer_ids)


async def _save_current_offer_row_versions(row_version: int) -> int:
    has_next = True
    page_size = settings.OFFERS_SYNC_PAGE_SIZE
    count = 0
    while has_next:
        try:
            response: GetChangedIdsV2Response = await v2_get_changed_announcements_ids(V2GetChangedAnnouncementsIds(
                row_version=row_version,
                top=page_size,
            ))
            offer_versions = response.announcements
        except ApiClientException:
            logger.exception('v2_get_changed_announcements_ids timeout')
            await asyncio.sleep(10)
            continue

        if not offer_versions:
            break

        await save_offer_row_versions(offer_versions)

        last_version = offer_versions[-1]
        row_version = last_version.row_version

        has_next = len(offer_versions) >= page_size
        count += len(offer_versions)

        logger.info('count %s  row_version %s', count, row_version)
        send_to_graphite(
            key='sync_offers.process_offers_count',
            value=count,
        )

    return count


async def _archive_offers(ids: List[int]) -> None:
    for offer_ids in grouper(ids, 100):
        await archive_missed_offers(list(filter(None, offer_ids)))
        await asyncio.sleep(settings.RESEND_JOB_DELAY)
        send_to_graphite(
            key='sync_offers.archived_offer_ids_progress',
            value=len(offer_ids),
        )
