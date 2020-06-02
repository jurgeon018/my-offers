from cian_web.exceptions import BrokenRulesException, Error

from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category, FlatType
from my_offers.repositories.price_estimator.entities.get_estimation_for_realtors_request import RoomsCount


def get_rooms_count(
        category: Category,
        flat_type: FlatType,
        rooms_count: int
) -> RoomsCount:
    if category in [Category.room_rent, Category.room_sale]:
        return RoomsCount.value_0
    if category == Category.bed_rent:
        return RoomsCount.value_10
    if flat_type == FlatType.studio:
        return RoomsCount.value_9
    if category == Category.flat_share_sale:
        return RoomsCount.value_8
    if flat_type == FlatType.open_plan:
        return RoomsCount.value_7
    if rooms_count >= 6:
        return RoomsCount.value_6
    if rooms_count == 5:
        return RoomsCount.value_5
    if rooms_count == 4:
        return RoomsCount.value_4
    if rooms_count == 3:
        return RoomsCount.value_3
    if rooms_count == 2:
        return RoomsCount.value_2
    if rooms_count == 1:
        return RoomsCount.value_1

    raise BrokenRulesException([Error(
        message='broken offer object_model, has not right room info',
        code='broken',
        key='rooms_count'
    )])
