from my_offers import entities
from my_offers.enums.offer_action_status import OfferActionStatus


async def archive_offer(request: entities.OfferActionRequest, realty_user_id: int) -> entities.OfferActionResponse:
    # todo: https://jira.cian.tech/browse/CD-73195
    return entities.OfferActionResponse(status=OfferActionStatus.ok)
