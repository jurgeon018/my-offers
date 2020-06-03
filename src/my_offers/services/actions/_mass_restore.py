import asyncio
from typing import List, Optional

from cian_web.exceptions import BrokenRulesException, Error
from simple_settings import settings

from my_offers import entities
from my_offers.entities.get_offers import Filter
from my_offers.repositories import monolith_cian_announcementapi, postgresql
from my_offers.repositories.monolith_cian_announcementapi.entities import (
    AnnouncementProgressDto,
    AnnouncementsActionsGetJobStatus,
    GetJobStatusResponse,
    RestoreRequest,
    RestoreResponse,
)
from my_offers.repositories.monolith_cian_announcementapi.entities.get_job_status_response import State as JobState
from my_offers.services.offers import get_filters


END_STATUSES = [
    JobState.completed,
    JobState.error,
]


# TODO: metrics for mass operations

async def mass_offers_restore(
    request: entities.OffersMassRestoreRequest,
    realty_user_id: int
) -> entities.OffersMassRestoreResponse:
    """ Массово восстановить все объявление для пользователя """
    # TODO: перенести в Actions: https://jira.cian.tech/browse/CD-82000
    # TODO: check rights

    offers_ids = request.offers_ids

    if not offers_ids and request.action_type.is_select:
        raise BrokenRulesException(errors=[Error(
            key='offers_ids',
            code='offers_ids_is_empty',
            message=f'offers_ids is empty with type `{request.action_type.name}`'
        )])

    #     if request.action_type.is_all:
    #         filters = await get_filters(
    #             user_id=realty_user_id,
    #             filters=Filter(status_tab=request.status_tab)
    #         )
    #         offers_ids = await postgresql.get_offers_ids_by_tab(
    #             filters=filters
    #         )
    #
    #     if not offers_ids:
    #         return entities.OffersMassRestoreResponse(offers=[])
    #
    #     offers_final_statuses = await _get_job_result(offers_ids=offers_ids, realty_user_id=realty_user_id)
    #     if offers_final_statuses:
    #         offers_statuses = [
    #             entities.OfferMassRestoreStatus(
    #                 offer_id=offer.id,
    #                 status=offer.state,
    #                 message=offer.error_message
    #             ) for offer in offers_final_statuses
    #         ]
    #
    #     # TODO: add offer_type in offers=[]   ???
    #     return entities.OffersMassRestoreResponse(offers=offers_statuses)
    #
    #
    # async def _get_job_result(*, offers_ids: List[int], realty_user_id: int) -> Optional[List[AnnouncementProgressDto]]:
    #     session: RestoreResponse = await monolith_cian_announcementapi.announcements_actions_restore(
    #         RestoreRequest(
    #             announcement_ids=offers_ids,
    #             user_id=realty_user_id
    #         )
    #     )
    #     # TODO: https://jira.cian.tech/browse/CD-81998
    #     while True:
    #         # TODO: add api version
    #         # {
    #         #     "message": "Задание не найдено",
    #         #     "errors": [
    #         #         {
    #         #             "message": "Задание не найдено",
    #         #             "key": "jobId",
    #         #             "code": null
    #         #         }
    #         #     ]
    #         # }
    #         await asyncio.sleep(settings.MASS_OFFERS_RESTORE_DELAY)
    #         job_status: GetJobStatusResponse = await monolith_cian_announcementapi.announcements_actions_get_job_status(
    #             AnnouncementsActionsGetJobStatus(
    #                 job_id=session.job_id,
    #                 user_id=realty_user_id
    #             )
    #         )
    #
    #         if job_status.state in END_STATUSES:
    #             break
    #
    #     return job_status.announcements_progress

    return entities.OffersMassRestoreResponse(offers=[])
