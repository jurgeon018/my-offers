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

    return entities.OffersMassRestoreResponse(offers=[])
