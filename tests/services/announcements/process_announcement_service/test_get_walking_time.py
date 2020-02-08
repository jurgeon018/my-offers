import pytest

from my_offers.services.announcement.process_announcement_service import _get_walking_time
from tests.utils import load_data


@pytest.mark.parametrize(
    ('geo', 'expected'),
    (
        (None, None),
        (load_data(__file__, 'geo_calc_undergrounds.json'), 20),
        (load_data(__file__, 'geo_undergrounds.json'), 13),
        (load_data(__file__, 'geo_transport_undergrounds.json'), 130),
    ),
)
def test__get_walking_time(geo, expected):
    # arrange & act
    result = _get_walking_time(geo)

    # assert
    assert result == expected
