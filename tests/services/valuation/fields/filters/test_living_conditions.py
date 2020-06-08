import pytest

from my_offers.repositories.price_estimator.entities import EstimationUserChosenFilters
from my_offers.repositories.price_estimator.entities.estimation_user_chosen_filters import Key, Value
from my_offers.services.valuation.fields.filters.living_сonditions import get_living_conditions


@pytest.mark.parametrize(
    ('children_allowed', 'pets_allowed', 'expected'),
    (
        (True, True, EstimationUserChosenFilters(
            key=Key.living_conditions,
            value=[Value.children_allowed, Value.pets_allowed]
        )),
        (True, False, EstimationUserChosenFilters(
            key=Key.living_conditions,
            value=[Value.children_allowed]
        )),
        (False, True, EstimationUserChosenFilters(
            key=Key.living_conditions,
            value=[Value.pets_allowed]
        )),
        (False, False, None),
        (None, None, None),
    )
)
def test_get_living_conditions(mocker, children_allowed, pets_allowed, expected):
    # arrange & act
    result = get_living_conditions(
        children_allowed=children_allowed,
        pets_allowed=pets_allowed,
    )

    # assert
    assert result == expected
