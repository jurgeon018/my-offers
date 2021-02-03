import logging

from my_offers.repositories.monolith_cian_ms_announcements import v2_get_changed_announcements_ids
from my_offers.repositories.monolith_cian_ms_announcements.entities import (
    GetChangedIdsV2Response,
    V2GetChangedAnnouncementsIds,
)
from my_offers.repositories.postgresql import (
    archive_missed_offers,
    clean_offer_row_versions,
    get_missed_offer_ids,
    get_outdated_offer_ids,
    save_offer_row_versions,
)
from my_offers.services.realty_resender._jobs import run_resend_task


logger = logging.getLogger(__name__)


async def sync_offers(row_version: int = 0):
    # очищаем таблицу с версиями объявлений
    await clean_offer_row_versions()

    # Сходить в C# announcemens и сохранить текущие версии объявлений
    await _save_current_offer_row_versions(row_version)

    # выбираем все объявки со старыми row_version и просим С# прислать их снова
    outdated_offer_ids = await get_outdated_offer_ids()
    await run_resend_task(outdated_offer_ids)

    # выбираем все объявки, которых у нас нет и просим С# прислать их снова
    missed_offer_ids = await get_missed_offer_ids()
    await run_resend_task(missed_offer_ids)

    # выбираем все объявки, которых нет в C# и отправляем их в архив
    await archive_missed_offers()


async def _save_current_offer_row_versions(row_version: int) -> None:
    has_next = True
    page_size = 3000
    count = 0
    while has_next:
        response: GetChangedIdsV2Response = await v2_get_changed_announcements_ids(V2GetChangedAnnouncementsIds(
            row_version=row_version,
            top=page_size,
        ))
        offer_versions = response.announcements

        if not offer_versions:
            break

        await save_offer_row_versions(offer_versions)

        last_version = offer_versions[-1]
        row_version = last_version.row_version

        has_next = len(offer_versions) >= page_size
        count += len(offer_versions)

        logger.info('count %s  row_version %s', count, row_version)
