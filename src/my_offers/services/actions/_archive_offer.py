from my_offers import entities
from my_offers.repositories.monolith_cian_announcementapi import v2_announcements_archive
from my_offers.repositories.monolith_cian_announcementapi.entities import ArchiveAnnouncementV2Request, ObjectModel
from my_offers.services.actions._action import OfferAction


class ArchiveOfferAction(OfferAction):
    def _get_action_code(self) -> str:
        return 'can_move_to_archive'

    async def _run_action(self, object_model: ObjectModel) -> None:
        await v2_announcements_archive(ArchiveAnnouncementV2Request(announcement_id=object_model.id))


async def archive_offer(request: entities.OfferActionRequest, realty_user_id: int) -> entities.OfferActionResponse:
    action = ArchiveOfferAction(offer_id=request.offer_id, user_id=realty_user_id)

    return await action.execute()
