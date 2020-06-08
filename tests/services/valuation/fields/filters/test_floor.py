import pytest

from my_offers.repositories.price_estimator.entities import EstimationUserChosenFilters
from my_offers.repositories.price_estimator.entities.estimation_user_chosen_filters import Key, Value
from my_offers.services.valuation.fields.filters.floor import get_floor


@pytest.mark.parametrize(
    ('floor_number', 'building_floors_count', 'expected'),
    (
        (1, 10, EstimationUserChosenFilters(
            key=Key.floor,
            value=[Value.floor_one]
        )),
        (2, 10, EstimationUserChosenFilters(
            key=Key.floor,
            value=[Value.floor_two]
        )),
        (10, 10, EstimationUserChosenFilters(
            key=Key.floor,
            value=[Value.floor_last]
        )),
        (6, 10, EstimationUserChosenFilters(
            key=Key.floor,
            value=[Value.floor_other]
        )),
        (6, None, EstimationUserChosenFilters(
            key=Key.floor,
            value=[Value.floor_other]
        )),
        (None, 6, None),
        (None, None, None),
    )
)
def test_get_floor(mocker, floor_number, building_floors_count, expected):
    # arrange & act
    result = get_floor(
        floor_number=floor_number,
        building_floors_count=building_floors_count,
    )

    # assert
    assert result == expected
