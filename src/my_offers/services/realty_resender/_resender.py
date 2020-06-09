import asyncio
import logging
from dataclasses import dataclass, field
from typing import List, Set, NamedTuple, Iterable

from cian_core.context import new_operation_id
from more_itertools import grouper
from itertools import zip_longest, chain
from simple_settings import settings

from my_offers.entities import OfferRowVersion
from my_offers.repositories import (
    monolith_cian_elasticapi,
    monolith_cian_ms_announcements,
    monolith_cian_realty,
    postgresql,
)
from my_offers.repositories.monolith_cian_elasticapi.entities import (
    ElasticResultIElasticAnnouncementElasticAnnouncementError as ElasticApiGetResponse, IElasticAnnouncement,
)
from my_offers.repositories.monolith_cian_elasticapi.entities import GetApiElasticAnnouncementGet
from my_offers.repositories.monolith_cian_ms_announcements.entities import V1GetChangedAnnouncementsIds
from my_offers.repositories.monolith_cian_realty.entities import (
    ApiV1ResendReportingMessagesGetJob,
    GetResendMessagesJobResponse,
    ResendAnnouncementsMessagesRequest,
)
from my_offers.repositories.monolith_cian_realty.entities.get_resend_messages_job_response import State as JobStatus
from my_offers.repositories.monolith_cian_realty.entities.resend_announcements_messages_request import BroadcastType


logger = logging.getLogger()

END_STATUSES = [
    JobStatus.finished,
    JobStatus.finished_with_errors,
]


@dataclass
class OfferData:
    ids: List[int] = field(default_factory=list)
    """Переданные объявления"""
    success_ids: List[int] = field(default_factory=list)
    """Объявления без ошибок"""
    errors_ids: List[int] = field(default_factory=list)
    """Объявсления с ошибками во время работы шедулера"""


class _OffersDiff(NamedTuple):
    not_found: Iterable[int]
    """Объявления не найденный в my=offers, но притутсвующие в Realty.Objects"""
    need_update: Iterable[int]
    """Объявления для которых не совпадают версии строк"""
    max_row_version: int
    """Максималынй row_version для текущей пачки объявлений"""


# первый раз запускаем с row_version = 0 (взять стартовый row_version до (полу)года)
# второй запуск будет с max(row_version) от текущей БД
# взять стартовый row_version до (полу)года
# row_version = 31749573344  # database

# session - uuid
# stats: check consistency, запросы к elasticapi (можем нагнуть эластик)

# 1. /v1/get-published-announcement-ids/
#   [http://swagger.dev3.cian.ru/?url=http://master.announcements.dev3.cian.ru/swagger/]
# 2. [v3] http://swagger.dev3.cian.ru/?url=http://master.monolith-cian-elasticapi.dev3.cian.ru/swagger/

# Get changed offers from row_version: 29910061494, count: 4164615

async def resend_offers(bulk_size: int) -> None:
    # TODO: max(row_version) - 1000 от changed_announcements_ids

    row_version = 29910061494  # await postgresql.get_last_row_version_for_offers()

    with new_operation_id() as operation_id:
        changed_offers_ids: List[int] = (await monolith_cian_ms_announcements.v1_get_changed_announcements_ids(
            V1GetChangedAnnouncementsIds(row_version=row_version)
        )).offers_ids
        changed_offers_ids_len = len(changed_offers_ids)

        logger.info('Get changed offers from row_version: %s, count: %s', row_version, changed_offers_ids_len)
        for offers_ids in grouper(changed_offers_ids, bulk_size):
            offers_ids = list(filter(None, offers_ids))

            logger.info('Get offers diff, progress %s/%s', len(offers_ids), changed_offers_ids_len)

            await asyncio.sleep(settings.GET_DIFF_DELAY)
            offers_diff = await _get_offers_diff(offers_ids=offers_ids)

            break


async def _get_offers_diff(offers_ids: List[int]) -> _OffersDiff:
    realty_offers: ElasticApiGetResponse = await monolith_cian_elasticapi.get_api_elastic_announcement_get(
        GetApiElasticAnnouncementGet(ids=offers_ids)
    )

    my_offers_ids = await postgresql.get_offers_row_version(offer_ids=offers_ids)
    realty_offers_set = {o.realty_object_id for o in realty_offers.success}
    my_offers_set = {o.offer_id for o in my_offers_ids}

    # realty_offers - offers_ids
    # ElasticAnnouncementError(code='announcement_not_found', message='Объявление от тестового пользователя')
    difference_for_requested = {
        err.realty_object_id for err in realty_offers.errors
        if err.code == 'announcement_not_found' and 'тестового пользователя' not in err.message
    }

    # realty_offers - my_offers_ids
    difference_for_my_offers = realty_offers_set - my_offers_set

    # realty_offers versions != my_offers versions
    difference_for_rows_versions = _get_row_versions_diff(realty_offers.success, my_offers_ids)

    print(
        f'difference_for_requested: {difference_for_requested}',
        f'difference_for_my_offers: {difference_for_my_offers}',
        f'difference_for_rows_versions: {difference_for_rows_versions}',

        sep='\n'
    )

    return _OffersDiff(
        not_found=difference_for_my_offers,
        need_update=difference_for_rows_versions,
        max_row_version=1111  # TODO


def _get_row_versions_diff(realty_offers: List[IElasticAnnouncement], my_offers: List[OfferRowVersion]) -> Set[int]:
    my_offers_map = {o.offer_id: o for o in my_offers}

    found_difference = set()

    for realty_offer in realty_offers:
        offer_id = realty_offer.realty_object_id
        my_offer = my_offers_map.get(offer_id)

        if not my_offer:
            continue

        if realty_offer.row_version > my_offer.row_version:
            found_difference.add(offer_id)

    return found_difference


async def _upsert_offers(offers_ids: List[int]): ...


async def _run_job(offers_ids: List[int]):
    job_id: int = (await monolith_cian_realty.api_v1_resend_reporting_messages_resend_announcements(
        ResendAnnouncementsMessagesRequest(
            ids=offers_ids,
            comment='',
            broadcast_type=BroadcastType(settings.RESEND_JOB_BROADCAST_TYPE)
        )
    )).id

    while True:
        await asyncio.sleep(settings.RESEND_JOB_REFRESH)
        job: GetResendMessagesJobResponse = await monolith_cian_realty.api_v1_resend_reporting_messages_get_job(
            ApiV1ResendReportingMessagesGetJob(id=job_id)
        )

        if job.state in END_STATUSES:
            #     "data": {
            #         "ids": [
            #             165489453,
            #             165489452,
            #             165489451,
            #             265489450
            #         ],
            #         "successIds": [
            #             165489453,
            #             165489452,
            #             165489451
            #         ],
            #         "errorIds": [
            #             265489450
            #         ]
            #     }
            if job.data:
                pass

            break
