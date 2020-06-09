import asyncio
import logging
from datetime import datetime
from typing import List

import pytz
from cian_json import json
from more_itertools import grouper
from simple_settings import settings

from my_offers.helpers.graphite import send_to_graphite
from my_offers.mappers.object_model import object_model_mapper
from my_offers.queue.producers import announcement_models_producer
from my_offers.repositories import monolith_cian_elasticapi, monolith_cian_realty
from my_offers.repositories.monolith_cian_elasticapi.entities import (
    ElasticResultIElasticAnnouncementElasticAnnouncementError as ElasticAnnouncementGetResponse,
)
from my_offers.repositories.monolith_cian_elasticapi.entities import GetApiElasticAnnouncementGet
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


async def save_offers_from_elasticapi(offers_ids: List[int]) -> None:
    """ Получить объялвения из elasticapi и отправить в очередь сохрарнения объявлений. """
    for offers in grouper(offers_ids, settings.ELASTIC_API_BULK_SIZE):
        offers = list(filter(None, offers))  # type: ignore
        await asyncio.sleep(settings.ELASTIC_API_DELAY)
        await _send_offers(offers_ids=offers)  # type: ignore

        send_to_graphite(
            key='resend_job_elasticapi.offers_count',
            value=len(offers),
            timestamp=datetime.now(pytz.utc).timestamp()
        )


async def _send_offers(offers_ids: List[int]) -> None:
    realty_offers: ElasticAnnouncementGetResponse = await monolith_cian_elasticapi.get_api_elastic_announcement_get(
        GetApiElasticAnnouncementGet(ids=offers_ids)
    )
    if realty_offers.errors:
        logger.warning('Error during call offers from elasticapi: %s', realty_offers.errors)

    if realty_offers.success:
        offers = [ro.object_model for ro in realty_offers.success]
        models = [object_model_mapper.map_from(json.loads(object_model)) for object_model in offers]

        for object_model in models:
            await announcement_models_producer(object_model)


async def run_resend_task(offers_ids: List[int]) -> None:
    """ Запросить досылку объялвений из Realty.Objects. Новые события придут в `announcements-temp`. """
    for offers in grouper(offers_ids, settings.RESEND_TASK_BULK_SIZE):
        offers = list(filter(None, offers))  # type: ignore
        await asyncio.sleep(settings.RESEND_JOB_DELAY)
        await _run_job(offers_ids=offers)  # type: ignore

        send_to_graphite(
            key='resend_job_realty_task.offers_count',
            value=len(offers),
            timestamp=datetime.now(pytz.utc).timestamp()
        )


async def _run_job(offers_ids: List[int]) -> None:
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
            if job.data:
                if error_ids := job.data.get('errorIds', []):
                    logger.warning('Error during resend offers: %s', error_ids)
            break
