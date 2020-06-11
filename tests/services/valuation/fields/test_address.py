import pytest
from cian_web.exceptions import BrokenRulesException

from my_offers.repositories.monolith_cian_announcementapi.entities import AddressInfo, Geo
from my_offers.repositories.monolith_cian_announcementapi.entities.address_info import Type
from my_offers.services.valuation.fields.address import get_address


def test_get_address():
    # arrange
    geo = Geo(
        address=[
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
    )

    # act
    result = get_address(geo=geo)

    # assert
    assert result == 'Москва, Никитский бульвар, 12'


def test_get_address_raise_exeption():
    # arrange & act
    with pytest.raises(BrokenRulesException) as exc_info:
        get_address(geo=None)

    # assert
    assert exc_info.value.errors[0].key == 'geo.address'
    assert exc_info.value.errors[0].code == 'valuation_not_poossible'
    assert exc_info.value.errors[0].message == 'broken offer object_model, has not right geo address'
