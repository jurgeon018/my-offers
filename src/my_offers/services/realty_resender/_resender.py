import asyncio
import logging
from dataclasses import dataclass, field
from typing import List, Tuple

from cian_core.context import new_operation_id
from simple_settings import settings

from my_offers.repositories import (
    monolith_cian_elasticapi,
    monolith_cian_ms_announcements,
    monolith_cian_realty,
    postgresql,
)
from my_offers.repositories.monolith_cian_elasticapi.entities import (
    ElasticResultIElasticAnnouncementElasticAnnouncementError as ElasticApiGetResponse,
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


logger = logging.getLogger(__name__)

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


# первый раз запускаем с row_version = 0 (взять стартовый row_version до (полу)года)
# второй запуск будет с max(row_version) от текущей БД

# session - uuid
# stats: check consistency, запросы к elasticapi
# можем нагнуть эластик

async def resend_offers(bulk_size: int = 1):
    # 1. /v1/get-published-announcement-ids/
    #   [http://swagger.dev3.cian.ru/?url=http://master.announcements.dev3.cian.ru/swagger/]
    # 2. [v3] http://swagger.dev3.cian.ru/?url=http://master.monolith-cian-elasticapi.dev3.cian.ru/swagger/

    # TODO: max(row_version) - 1000 от changed_announcements_ids

    # взять стартовый row_version до (полу)года
    row_version = 31749573344  # database
    with new_operation_id() as operation_id:
        changed_offers_ids: List[int] = (await monolith_cian_ms_announcements.v1_get_changed_announcements_ids(
            V1GetChangedAnnouncementsIds(row_version=row_version)
        )).offers_ids

        # offers_ids = [225540774]
        changed_offers_ids = changed_offers_ids[:50]

        await _get_offers_diff(offers_ids=changed_offers_ids)


async def _get_offers_diff(offers_ids: List[int]) -> Tuple[List[int], List[int]]:
    realty_offers: ElasticApiGetResponse = await monolith_cian_elasticapi.get_api_elastic_announcement_get(
        GetApiElasticAnnouncementGet(ids=offers_ids)
    )
    if realty_offers.errors:
        logger.warning('Error during call elasticapi: %s', realty_offers.errors)

    my_offers_ids = await postgresql.get_offers_row_version(offer_ids=offers_ids)
    realty_offers_set = {o.realty_object_id for o in realty_offers.success}
    my_offers_set = {o.offer_id for o in my_offers_ids}

    if difference := realty_offers_set.symmetric_difference(my_offers_set): pass

    # realty_offers - offers_ids
    difference_for_requested = {
        err.realty_object_id for err in realty_offers.errors
        if err.code == 'announcement_not_found'
    }

    # realty_offers - my_offers_ids
    difference_for_my_offers = realty_offers_set - my_offers_set

    # my_offers_ids - realty_offers ???
    difference_for_realty = my_offers_set - realty_offers_set

    # realty_offers versions != my_offers versions
    difference_for_rows_versions = _check_row_versions(...)

    print(
        f'difference_for_requested: {difference_for_requested}',
        f'difference_for_my_offers: {difference_for_my_offers}',
        f'difference_for_realty: {difference_for_realty}',

        f'difference_for_realty == difference_for_requested: {difference_for_realty == difference_for_requested}',

        sep='\n'
    )
    return [], []


def _check_row_versions(*args):
    return ''


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
