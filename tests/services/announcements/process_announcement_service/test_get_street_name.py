import pytest

from my_offers.repositories.monolith_cian_announcementapi.entities import AddressInfo
from my_offers.repositories.monolith_cian_announcementapi.entities.address_info import Type
from my_offers.services.announcement.fields.street_name import get_street_name


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
                ),
                AddressInfo(
                    id=288556,
                    name='Большая Садовая',
                    type=Type.street,
                    full_name='Большая Садовая улица',
                    short_name='Большая Садовая ул.',
                    is_forming_address=True,
                )
            ],
            'Большая Садовая',
        )
    )
)
def test__get_street_name(address, expected):
    # arrange & act
    result = get_street_name(address)

    # assert
    assert result == expected
