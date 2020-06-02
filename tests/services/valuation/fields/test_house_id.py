import pytest
from cian_web.exceptions import BrokenRulesException

from my_offers.repositories.monolith_cian_announcementapi.entities import AddressInfo
from my_offers.repositories.monolith_cian_announcementapi.entities.address_info import Type
from my_offers.services.valuation.fields.house_id import get_house_id


def test_get_house_id():
    # arrange & act
    address = [
        AddressInfo(
            id=1,
            name='Москва',
            type=Type.location,
            full_name='Москва',
            short_name='Москва',
            location_type_id=1,
            is_forming_address=True
        ),
        AddressInfo(
            id=3127,
            name='Никитский',
            type=Type.street,
            full_name='Никитский бульвар',
            short_name='Никитский бул.',
            is_forming_address=True
        ),
        AddressInfo(
            id=1691187,
            name='12',
            type=Type.house,
            full_name='12',
            short_name='12',
            is_forming_address=True
        )
    ]
    result = get_house_id(address=address)

    # assert
    assert result == 1691187


def test_get_house_id_raise_exeption():
    # arrange & act
    address_without_house = [
        AddressInfo(
            id=1,
            name='Москва',
            type=Type.location,
            full_name='Москва',
            short_name='Москва',
            location_type_id=1,
            is_forming_address=True
        ),
        AddressInfo(
            id=3127,
            name='Никитский',
            type=Type.street,
            full_name='Никитский бульвар',
            short_name='Никитский бул.',
            is_forming_address=True
        )
    ]

    with pytest.raises(BrokenRulesException) as exc_info:
        get_house_id(address=address_without_house)

    # assert
    assert exc_info.value.errors[0].key == 'house_id'
    assert exc_info.value.errors[0].message == 'offer object_model does not have house in address, valuation can not ' \
                                               'be provided without house_id'
