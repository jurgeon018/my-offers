from datetime import datetime

import pytest

from my_offers.helpers.time import get_left_time_display


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
