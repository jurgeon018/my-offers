import pytest

from my_offers.repositories.monolith_cian_announcementapi.entities import BargainTerms, ObjectModel, Phone
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category, RepairType
from my_offers.repositories.price_estimator.entities import EstimationUserChosenFilters
from my_offers.repositories.price_estimator.entities.estimation_user_chosen_filters import Key, Value
from my_offers.services.valuation.helpers.valuation_filters import get_valuation_filters


@pytest.mark.parametrize(
    ('object_model', 'expected'),
    (
        (
            ObjectModel(
                bargain_terms=BargainTerms(price=123),
                category=Category.flat_rent,
                phones=[Phone(country_code='1', number='12312')],
                floor_number=1,
                has_washer=True,
                has_conditioner=True,
                has_fridge=False,
                pets_allowed=True,
                repair_type=RepairType.no,
            ),
            [
                EstimationUserChosenFilters(
                    key=Key.floor,
                    value=[Value.floor_one]
                ),
                EstimationUserChosenFilters(
                    key=Key.amenities,
                    value=[
                        Value.washing_machine,
                        Value.conditioner,
                    ]
                ),
                EstimationUserChosenFilters(
                    key=Key.living_conditions,
                    value=[Value.pets_allowed]
                ),
                EstimationUserChosenFilters(
                    key=Key.repair_type,
                    value=[Value.repair_type_without]
                )
            ],
        ),
        (
            ObjectModel(
                bargain_terms=BargainTerms(price=123),
                category=Category.flat_rent,
                phones=[Phone(country_code='1', number='12312')],
            ),
            None
        )

    )
)
def test_get_valuation_filters(mocker, object_model, expected):
    # arrange & act
    result = get_valuation_filters(object_model=object_model)

    # assert
    assert result == expected
