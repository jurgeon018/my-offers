from datetime import datetime

import pytest
import pytz
from cian_helpers.timezone import TIMEZONE

from my_offers.helpers.time import get_aware_date
from my_offers.services.offer_view.helpers.time import get_left_time_display


@pytest.mark.parametrize(
    ('current', 'end', 'expected'),
    (
        (datetime(2020, 3, 5, 10), datetime(2020, 3, 10, 10), '5 дней'),
        (datetime(2020, 3, 5, 10), datetime(2020, 3, 5, 12), '2 часа'),
        (datetime(2020, 3, 5, 12), datetime(2020, 3, 5, 12, 30), 'менее 1 часа'),
    )
)
def test_get_left_time_display(mocker, current, end, expected):
    # arrange & act
    result = get_left_time_display(current=current, end=end)

    # assert
    assert result == expected


def test_get_left_time_display__date__value_error(mocker):
    # arrange
    current = datetime(2020, 3, 5, 12)
    end = datetime(2019, 3, 5, 12)

    # act & assert
    with pytest.raises(ValueError):
        get_left_time_display(current=current, end=end)


@pytest.mark.parametrize(
    ('date', 'expected'),
    (
        (None, None),
        (datetime(2020, 3, 30, 10), TIMEZONE.localize(datetime(2020, 3, 30, 10))),
        (datetime(2020, 3, 30, 10, tzinfo=pytz.UTC), datetime(2020, 3, 30, 10, tzinfo=pytz.UTC)),
    )
)
def test_get_aware_date(mocker, date, expected):
    # arrange & act
    result = get_aware_date(date)

    # assert
    assert result == expected
