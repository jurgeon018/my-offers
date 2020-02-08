import pytest

from my_offers.services.announcement.process_announcement_service import _get_total_area


@pytest.mark.parametrize(
    ('total_area', 'land', 'expected'),
    (
        (
            None,
            {
                'area': 1.0,
                'status': 'industryTransportCommunications',
                'areaUnitType': 'hectare',
            },
            10000,
        ),
        (
            None,
            None,
            None,
        ),
        (
            300,
            None,
            300,
        ),
    ),
)
def test__get_total_area(total_area, land, expected):
    # arrange & act
    result = _get_total_area(total_area=total_area, land=land)

    # assert
    assert result == expected
