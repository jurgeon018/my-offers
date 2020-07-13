from typing import List

from simple_settings import settings

from my_offers import entities
from my_offers.repositories import monolith_cian_announcementapi
from my_offers.repositories.monolith_cian_announcementapi.entities import ChangeOwnerRequest
from my_offers.services.actions._action import MassActions


class OffersChangePublisherAction(MassActions):

    def __init__(self, *, offers_ids: List[int], actor_id: int, new_owner_id: int) -> None:
        super().__init__(offers_ids=offers_ids, actor_id=actor_id)
        self.new_owner_id = new_owner_id

    async def _run_job(self) -> int:
        session = await monolith_cian_announcementapi.announcements_actions_v1_change_owner(
            ChangeOwnerRequest(
                actor_id=self.actor_id,
                announcement_ids=self.offers_ids,
                new_owner_id=self.new_owner_id
            )
        )
        return session.job_id


async def change_offers_publisher(
        request: entities.OffersChangePublisherRequest,
        realty_user_id: int
) -> entities.OffersChangePublisherResponse:
    """ Сменить владельца для пачки объялвений. Выполнить действие может только мастер аккаунт. """

    if not request.offers_ids:
        return entities.OffersChangePublisherResponse(offers=[])

    change_publisher_action = OffersChangePublisherAction(
        actor_id=realty_user_id,
        offers_ids=request.offers_ids,
        new_owner_id=request.user_id
    )
    result = await change_publisher_action.execute(
        delay=settings.MASS_OFFERS_CHANGE_OWNERS_DELAY
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
