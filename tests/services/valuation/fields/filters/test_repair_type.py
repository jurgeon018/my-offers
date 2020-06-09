import pytest

from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import RepairType
from my_offers.repositories.price_estimator.entities import EstimationUserChosenFilters
from my_offers.repositories.price_estimator.entities.estimation_user_chosen_filters import Key, Value
from my_offers.services.valuation.fields.filters.repair_type import get_repair_type


@pytest.mark.parametrize(
    ('repair_type', 'expected'),
    (
        (RepairType.no, EstimationUserChosenFilters(
            key=Key.repair_type,
            value=[Value.repair_type_without]
        )),
        (RepairType.euro, EstimationUserChosenFilters(
            key=Key.repair_type,
            value=[Value.repair_type_euro]
        )),
        (RepairType.design, EstimationUserChosenFilters(
            key=Key.repair_type,
            value=[Value.repair_type_design]
        )),
        (RepairType.cosmetic, EstimationUserChosenFilters(
            key=Key.repair_type,
            value=[Value.repair_type_cosmetic]
        )),
        (None, None)

    )
)
def test_get_price(mocker, repair_type, expected):
    # arrange & act
    result = get_repair_type(repair_type=repair_type)

    # assert
    assert result == expected
