import asyncio
from typing import List

from simple_settings import settings

from my_offers import entities
from my_offers.repositories import monolith_cian_announcementapi
from my_offers.repositories.monolith_cian_announcementapi.entities import (
    AnnouncementsActionsV1GetJobStatus,
    ChangeOwnerRequest,
    ChangeOwnerResponse,
    GetJobStatusResponse,
)
from my_offers.repositories.monolith_cian_announcementapi.entities.announcement_progress_dto import (
    AnnouncementProgressDto,
)
from my_offers.repositories.monolith_cian_announcementapi.entities.get_job_status_response import State as JobState


END_STATUSES = [
    JobState.completed,
    JobState.error,
]


async def change_offers_publisher(
    request: entities.OffersChangePublisherRequest,
    realty_user_id: int
) -> entities.OffersChangePublisherResponse:
    """ Сменить владельца для пачки объялвений. Выполнить действие может только мастер аккаунт. """

    if not request.offers_ids:
        return entities.OffersChangePublisherResponse(offers=[])

    result = await _run_job(
        actor_id=realty_user_id,
        offers_ids=request.offers_ids,
        new_owner_id=request.user_id
    )

    offers = [
        entities.OffersChangePublisherStatus(
            offer_id=offer.id,
            status=offer.state,
            message=offer.error_message
        ) for offer in result
    ]

    return entities.OffersChangePublisherResponse(
        offers=offers
    )


async def _run_job(*, offers_ids: List[int], actor_id: int, new_owner_id: int) -> List[AnnouncementProgressDto]:
    session: ChangeOwnerResponse = await monolith_cian_announcementapi.announcements_actions_v1_change_owner(
        ChangeOwnerRequest(
            actor_id=actor_id,
            announcement_ids=offers_ids,
            new_owner_id=new_owner_id
        )
    )

    while True:
        await asyncio.sleep(settings.MASS_OFFERS_CHANGE_OWNERS_DELAY)
        job_status: GetJobStatusResponse = await monolith_cian_announcementapi.announcements_actions_v1_get_job_status(
            AnnouncementsActionsV1GetJobStatus(
                job_id=session.job_id,
                user_id=actor_id
            )
        )

        if job_status.state in END_STATUSES:
            break

    return job_status.announcements_progress or []
