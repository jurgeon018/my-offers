from cian_web.exceptions import BrokenRulesException, Error

from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category, FlatType
from my_offers.repositories.price_estimator.entities.get_estimation_for_realtors_request import RoomsCount


OFFER_ROOMS_VALUATION_ROOMS = {
    1: RoomsCount.value_1,
    2: RoomsCount.value_2,
    3: RoomsCount.value_3,
    4: RoomsCount.value_4,
    5: RoomsCount.value_5,
}


def get_rooms_count(
        *,
        category: Category,
        flat_type: FlatType,
        rooms_count: int
) -> RoomsCount:
    if category in [Category.room_rent, Category.room_sale]:
        return RoomsCount.value_0
    if flat_type == FlatType.studio:
        return RoomsCount.value_9
    if flat_type == FlatType.open_plan:
        return RoomsCount.value_7
    if rooms_count >= 6:
        return RoomsCount.value_6

    result = OFFER_ROOMS_VALUATION_ROOMS.get(rooms_count)

    if result is None:
        raise BrokenRulesException([
            Error(
                message='broken offer object_model, has not right room info',
                code='valuation_not_poossible',
                key='rooms_count'
            )
        ])

    return result
