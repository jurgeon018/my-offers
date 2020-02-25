from my_offers import entities
from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel
from my_offers.repositories.postgresql.object_model import get_object_model
from my_offers.services.get_master_user_id import get_master_user_id


async def delete_offer(request: entities.OfferActionRequest, realty_user_id: int):
    object_model = get_object_model({
        'offer_id': request.offer_id,
        'master_user_id': await get_master_user_id(realty_user_id),
    })


async def _check_rights(user_id: int, object_model: ObjectModel) -> None:
    # todo: https://jira.cian.tech/browse/CD-74186
