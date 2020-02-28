import pytest

from my_offers.repositories.monolith_cian_announcementapi.entities import Land
from my_offers.repositories.monolith_cian_announcementapi.entities.land import AreaUnitType, Status
from my_offers.services.announcement.fields.total_area import get_total_area


@pytest.mark.parametrize(
    ('total_area', 'land', 'expected'),
    (
        (
            None,
            Land(
                area=1.0,
                status=Status.industry_transport_communications,
                area_unit_type=AreaUnitType.hectare,
            ),
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
    result = get_total_area(total_area=total_area, land=land)

    # assert
    assert result == expected
