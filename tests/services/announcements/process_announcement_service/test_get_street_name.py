import pytest

from my_offers.services.announcement.fields.street_name import get_street_name


@pytest.mark.parametrize(
    ('address', 'expected'),
    (
        (None, None),
        (
            [{
                'id': 4606,
                'name': 'Ростовская',
                'type': 'location',
                'fullName': 'Ростовская область',
                'shortName': 'Ростовская область',
                'locationTypeId': 2,
                'isFormingAddress': True
            }, {
                'id': 4959,
                'name': 'Ростов-на-Дону',
                'type': 'location',
                'fullName': 'Ростов-на-Дону',
                'shortName': 'Ростов-на-Дону',
                'locationTypeId': 1,
                'isFormingAddress': True
            }, {
                'id': 288556,
                'name': 'Большая Садовая',
                'type': 'street',
                'fullName': 'Большая Садовая улица',
                'shortName': 'Большая Садовая ул.',
                'isFormingAddress': True
            }, {
                'id': 2045030,
                'name': '73',
                'type': 'house',
                'fullName': '73',
                'shortName': '73',
                'isFormingAddress': True
            }],
            'Большая Садовая',
        )
    )
)
def test__get_street_name(address, expected):
    # arrange & act
    result = get_street_name(address)

    # assert
    assert result == expected
