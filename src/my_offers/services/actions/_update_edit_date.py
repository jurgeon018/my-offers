from cian_web.exceptions import BrokenRulesException, Error

from my_offers import entities
from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel
from my_offers.services import announcement_api
from my_offers.services.actions._action import OfferAction


class UpdateEditDateOfferAction(OfferAction):
    async def _run_action(self, object_model: ObjectModel) -> None:
        result = await announcement_api.update_edit_date([object_model.id])
        if not result[object_model.id]:
            raise BrokenRulesException([
                Error(
                    message='Не удалось обновить дату',
                    code='update_edit_date_error',
                    key='offer_id'
                )
            ])


async def update_edit_date(request: entities.OfferActionRequest, realty_user_id: int) -> entities.OfferActionResponse:
    action = UpdateEditDateOfferAction(offer_id=request.offer_id, user_id=realty_user_id)

    return await action.execute()
