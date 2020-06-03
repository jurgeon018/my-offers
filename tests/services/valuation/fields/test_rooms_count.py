import pytest
from cian_web.exceptions import BrokenRulesException

from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category, FlatType
from my_offers.repositories.price_estimator.entities.get_estimation_for_realtors_request import RoomsCount
from my_offers.services.valuation.fields.rooms_count import get_rooms_count


@pytest.mark.parametrize(
    ('category', 'flat_type', 'rooms_count', 'expected'),
    (
        (Category.room_rent, FlatType.rooms, 1, RoomsCount.value_0),
        (Category.room_sale, FlatType.rooms, 1, RoomsCount.value_0),
        (Category.flat_rent, FlatType.studio, 1, RoomsCount.value_9),
        (Category.flat_sale, FlatType.open_plan, 1, RoomsCount.value_7),
        (Category.flat_sale, FlatType.rooms, 6, RoomsCount.value_6),
        (Category.flat_rent, FlatType.rooms, 10, RoomsCount.value_6),
        (Category.flat_sale, FlatType.rooms, 5, RoomsCount.value_5),
        (Category.flat_rent, FlatType.rooms, 4, RoomsCount.value_4),
        (Category.flat_sale, FlatType.rooms, 3, RoomsCount.value_3),
        (Category.flat_rent, FlatType.rooms, 2, RoomsCount.value_2),
        (Category.flat_sale, FlatType.rooms, 1, RoomsCount.value_1),
    )
)
def test_get_rooms_count(mocker, category, flat_type, rooms_count, expected):
    # arrange & act
    result = get_rooms_count(category=category, flat_type=flat_type, rooms_count=rooms_count)

    # assert
    assert result == expected


def test_get_rooms_count_raise_exeption():
    # arrange & act
    with pytest.raises(BrokenRulesException) as exc_info:
        get_rooms_count(
            category=Category.flat_sale,
            flat_type=FlatType.rooms,
            rooms_count=0,
        )

    # assert
    assert exc_info.value.errors[0].key == 'rooms_count'
    assert exc_info.value.errors[0].code == 'valuation_not_poossible'
    assert exc_info.value.errors[0].message == 'broken offer object_model, has not right room info'
