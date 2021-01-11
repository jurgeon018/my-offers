import pytest
from cian_test_utils import v

from my_offers.helpers.title import _get_floors, get_offer_title, get_properties, get_workplace_title
from my_offers.repositories.monolith_cian_announcementapi.entities import (
    BargainTerms,
    Building,
    Land,
    ObjectModel,
    Phone,
)
from my_offers.repositories.monolith_cian_announcementapi.entities.land import AreaUnitType
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import (
    Category,
    CoworkingOfferType,
    FlatType,
)


@pytest.mark.parametrize(
    ('floor_number', 'floors_count', 'expected'),
    (
        (1, 2, '1/2\xa0этаж'),
        (3, None, '3\xa0этаж'),
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
            'Офис, 100\xa0м²'
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
            'Офис, от\xa07\xa0до\xa0100\xa0м²'
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
            'Земельный участок, 77\xa0сот.'
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
        (
            v(ObjectModel(
                id=111,
                bargain_terms=BargainTerms(price=123.0),
                category=Category.office_rent,
                phones=[Phone(country_code='1', number='12312')],
                user_id=222,
                total_area=100.0,
                workplace_count=10,
                floor_number=1,
                building=v(Building(floors_count=19)),
                coworking_offer_type=CoworkingOfferType.office,
            )),
            'Отдельный офис 100\xa0м² на 10 чел., 1/19 этаж'
        ),
        (
            v(ObjectModel(
                id=111,
                bargain_terms=BargainTerms(price=123.0),
                category=Category.office_rent,
                phones=[Phone(country_code='1', number='12312')],
                user_id=222,
                total_area=100.0,
                workplace_count=None,
                coworking_offer_type=CoworkingOfferType.office,
            )),
            'Отдельный офис 100\xa0м²'
        ),
    )
)
def test_get_title(object_model, expected):
    # arrange & act
    result = get_offer_title(object_model)

    # assert
    assert result == expected


@pytest.mark.parametrize(
    'coworking_offer_type, floor_number, floor_from, floor_to, expected',
    (
            (CoworkingOfferType.fixed_workplace, 12, None, None, ('10 закреплённых рабочих мест', 12)),
            (CoworkingOfferType.flexible_workplace, 12, None, None, ('10 незакреплённых рабочих мест', 12)),
            (CoworkingOfferType.fixed_workplace, None, None, None, ('10 закреплённых рабочих мест', None)),
            (CoworkingOfferType.flexible_workplace, None, None, None, ('10 незакреплённых рабочих мест', None)),
            (CoworkingOfferType.fixed_workplace, None, 1, 5, ('10 закреплённых рабочих мест', '1-5')),
            (CoworkingOfferType.flexible_workplace, None, 1, 5, ('10 незакреплённых рабочих мест', '1-5')),
    )
)
def test_workplace_title(coworking_offer_type, floor_number, floor_to, floor_from, expected):
    """Проверка возвращаемого title и floor_number, для fixed/flex workplace объялений."""
    # arrange
    object_model = v(ObjectModel(
        id=111,
        bargain_terms=BargainTerms(price=123.0),
        category=Category.office_rent,
        phones=[Phone(country_code='1', number='12312')],
        user_id=222,
        total_area=100.0,
        workplace_count=10,
        floor_number=1,
        building=v(Building(floors_count=19)),
        coworking_offer_type=coworking_offer_type,
        floor_to=floor_to,
        floor_from=floor_from,
    ))
    # act & assert
    assert get_workplace_title(object_model=object_model, floor_number=floor_number) == expected


@pytest.mark.parametrize(
    'coworking_offer_type, floor_from, floor_to, expected',
    (
            (
                    CoworkingOfferType.fixed_workplace,
                    1,
                    6,
                    ['10 закреплённых рабочих мест', '100\xa0м²', '1-6/19\xa0этаж']
            ),
            (
                    CoworkingOfferType.flexible_workplace,
                    1,
                    6,
                    ['10 незакреплённых рабочих мест', '100\xa0м²', '1-6/19\xa0этаж']
            ),
    )
)
def test_get_properties_with_workplace_title(coworking_offer_type, floor_to, floor_from, expected):
    # arrange
    object_model = v(ObjectModel(
        id=111,
        bargain_terms=BargainTerms(price=123.0),
        category=Category.office_rent,
        phones=[Phone(country_code='1', number='12312')],
        user_id=222,
        total_area=100.0,
        workplace_count=10,
        floor_number=None,
        building=v(Building(floors_count=19)),
        coworking_offer_type=coworking_offer_type,
        floor_to=floor_to,
        floor_from=floor_from,
    ))
    # act & assert
    assert get_properties(object_model=object_model) == expected
