import pytest

from my_offers.helpers.title import _get_floors, get_title
from my_offers.repositories.monolith_cian_announcementapi.entities import BargainTerms, Land, ObjectModel, Phone
from my_offers.repositories.monolith_cian_announcementapi.entities.land import AreaUnitType
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category, FlatType


@pytest.mark.parametrize(
    ('floor_number', 'floors_count', 'expected'),
    (
        (1, 2, '1/2 этаж'),
        (3, None, '3 этаж'),
        (None, 10, None),
        (-1, 10, 'полуподвал')
    )
)
def test__get_floors(floor_number, floors_count, expected):
    # arrange & act
    result = _get_floors(floor_number=floor_number, floors_count=floors_count)

    # assert
    assert result == expected


@pytest.mark.parametrize(
    ('object_model', 'expected'),
    (
        (
            ObjectModel(
                id=111,
                bargain_terms=BargainTerms(price=123),
                category=Category.office_sale,
                phones=[Phone(country_code='1', number='12312')],
                user_id=222,
                total_area=100,
            ),
            'Офис, 100 м²'
        ),
        (
            ObjectModel(
                id=111,
                bargain_terms=BargainTerms(price=123),
                category=Category.office_sale,
                phones=[Phone(country_code='1', number='12312')],
                user_id=222,
                total_area=100,
                can_parts=True,
                min_area=7,
            ),
            'Офис, от 7 до 100 м²'
        ),
        (
            ObjectModel(
                id=111,
                bargain_terms=BargainTerms(price=123),
                category=Category.land_sale,
                phones=[Phone(country_code='1', number='12312')],
                user_id=222,
                total_area=100,
                land=Land(area=77, area_unit_type=AreaUnitType.sotka),
            ),
            'Земельный участок, 77 сот.'
        ),
        (
            ObjectModel(
                id=111,
                bargain_terms=BargainTerms(price=123),
                category=Category.flat_sale,
                phones=[Phone(country_code='1', number='12312')],
                user_id=222,
                flat_type=FlatType.studio,
            ),
            'Квартира-студия'
        ),
    )
)
def test_get_title(object_model, expected):
    # arrange & act
    result = get_title(object_model)

    # assert
    assert result == expected
