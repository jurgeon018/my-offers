import pytest

from my_offers.repositories.price_estimator.entities import EstimationUserChosenFilters
from my_offers.repositories.price_estimator.entities.estimation_user_chosen_filters import Key, Value
from my_offers.services.valuation.fields.filters.amenities import get_amenities


@pytest.mark.parametrize(
    ('kitchen_furniture', 'washer', 'tv', 'fridge', 'conditioner', 'expected'),
    (
        (True, True, True, True, True, EstimationUserChosenFilters(
            key=Key.amenities,
            value=[
                Value.kitchen_furniture,
                Value.washing_machine,
                Value.tv,
                Value.fridge,
                Value.conditioner,
            ]
        )),
        (True, False, False, False, None, EstimationUserChosenFilters(
            key=Key.amenities,
            value=[Value.kitchen_furniture]
        )),
        (False, True, None, False, False, EstimationUserChosenFilters(
            key=Key.amenities,
            value=[Value.washing_machine]
        )),
        (False, None, True, False, False, EstimationUserChosenFilters(
            key=Key.amenities,
            value=[Value.tv]
        )),
        (None, False, False, True, False, EstimationUserChosenFilters(
            key=Key.amenities,
            value=[Value.fridge]
        )),
        (False, False, False, None, True, EstimationUserChosenFilters(
            key=Key.amenities,
            value=[Value.conditioner]
        )),
        (False, True, False, True, False, EstimationUserChosenFilters(
            key=Key.amenities,
            value=[
                Value.washing_machine,
                Value.fridge
            ]
        )),
        (True, False, True, False, True, EstimationUserChosenFilters(
            key=Key.amenities,
            value=[
                Value.kitchen_furniture,
                Value.tv,
                Value.conditioner
            ]
        )),
        (False, False, False, False, False, None),
        (None, None, None, None, None, None)
    )
)
def test_get_living_conditions(mocker, kitchen_furniture, washer, tv, fridge, conditioner, expected):
    # arrange & act
    result = get_amenities(
        kitchen_furniture=kitchen_furniture,
        washer=washer,
        tv=tv,
        fridge=fridge,
        conditioner=conditioner,
    )

    # assert
    assert result == expected
