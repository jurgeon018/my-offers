from cian_web.exceptions import BrokenRulesException, Error

from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel
from my_offers.repositories.postgresql.object_model import get_object_model
from my_offers.services.offers import get_user_filter


async def load_object_model(*, user_id: int, offer_id: int) -> ObjectModel:
    offer_filter = await get_user_filter(user_id)
    offer_filter['offer_id'] = offer_id
    object_model = await get_object_model(offer_filter)

    if not object_model:
        raise BrokenRulesException([
            Error(
                message='Объявление не найдено',
                code='not_found',
                key='offer_id'
            )
        ])

    return object_model
