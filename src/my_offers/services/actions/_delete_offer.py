from my_offers import entities, enums
from my_offers.helpers import category
from my_offers.helpers.user_ids import get_realty_id_by_cian_id
from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel
from my_offers.repositories.monolith_cian_realty import api_announcement_set_deleted
from my_offers.repositories.monolith_cian_realty.entities import AnnouncementChangeStatus
from my_offers.repositories.monolith_cian_realty.entities.announcement_change_status import AnnouncementType
from my_offers.services.actions._action import OfferAction


class AnnouncementTypeError(Exception):
    pass


class DeleteOfferAction(OfferAction):
    async def _run_action(self, object_model: ObjectModel) -> None:
        offer_type, deal_type = category.get_types(object_model.category)
        await api_announcement_set_deleted(
            AnnouncementChangeStatus(
                realty_object_id=object_model.id,
                announcement_type=self._get_type_for_asp(offer_type=offer_type, deal_type=deal_type),
                cian_announcement_id=object_model.cian_id,
                cian_user_id=get_realty_id_by_cian_id(self.user_id),
            )
        )

    @staticmethod
    def _get_type_for_asp(*, offer_type: enums.OfferType, deal_type: enums.DealType) -> AnnouncementType:
        if offer_type.is_flat:
            return AnnouncementType.flat if deal_type.is_rent else AnnouncementType.flat2

        if offer_type.is_suburban:
            return AnnouncementType.suburbian

        if offer_type.is_commercial:
            return AnnouncementType.office

        raise AnnouncementTypeError('Сan not determine AnnouncementType')


async def delete_offer(request: entities.OfferActionRequest, realty_user_id: int) -> entities.OfferActionResponse:
    action = DeleteOfferAction(offer_id=request.offer_id, user_id=realty_user_id)

    return await action.execute()
