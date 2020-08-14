import pytest

from my_offers.repositories.monolith_cian_announcementapi.entities import AddressInfo
from my_offers.repositories.monolith_cian_announcementapi.entities.address_info import Type
from my_offers.services.similars.helpers.house import get_house_id


@pytest.mark.parametrize(
    ('address', 'expected'),
    (
        (None, None),
        (
            [
                AddressInfo(
                    id=4959,
                    name='Ростов-на-Дону',
                    type=Type.location,
                    full_name='Ростов-на-Дону',
                    short_name='Ростов-на-Дону',
                    location_type_id=1,
                    is_forming_address=True,
                )
            ],
            None
        ),
        (
            [
                AddressInfo(
                    id=4959,
                    name='Ростов-на-Дону',
                    type=Type.location,
                    full_name='Ростов-на-Дону',
                    short_name='Ростов-на-Дону',
                    location_type_id=1,
                    is_forming_address=True,
                ),
                AddressInfo(
                    id=2412178,
                    name='8',
                    type=Type.house,
                    full_name='8',
                    short_name='8',
                    is_forming_address=True,
                )
            ],
            2412178,
        )
    )
)
def test__get_house_id(address, expected):
    # arrange & act
    result = get_house_id(address)

    # assert
    assert result == expected
