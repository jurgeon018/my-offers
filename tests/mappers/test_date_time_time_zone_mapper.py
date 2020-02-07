from datetime import datetime

import pytest
import pytz
from cian_helpers.timezone import TIMEZONE

from my_offers.mappers.date_time import DateTimeTimeZoneMapper


@pytest.mark.parametrize(
    ('src', 'expected'),
    (
        ('2020-02-05T13:36:13.317', TIMEZONE.localize(datetime(2020, 2, 5, 13, 36, 13, 317000))),
        ('2020-02-05T13:36:13.31', TIMEZONE.localize(datetime(2020, 2, 5, 13, 36, 13, 310000))),
        ('2020-02-05T13:36:13.317+03:00', TIMEZONE.localize(datetime(2020, 2, 5, 13, 36, 13, 317000))),
        ('2020-02-05T13:36:13.317+00:00', datetime(2020, 2, 5, 13, 36, 13, 317000, tzinfo=pytz.UTC)),
    ),
)
def test_date_time_time_zone_mapper(src, expected):
    # arrange
    mapper = DateTimeTimeZoneMapper()

    # act
    result = mapper.map_from(src)

    # assert
    assert result == expected
