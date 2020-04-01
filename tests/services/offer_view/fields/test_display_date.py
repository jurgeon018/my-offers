from datetime import datetime

import pytest
from cian_helpers.timezone import TIMEZONE

from my_offers.services.offer_view.fields.display_date import get_display_date


@pytest.mark.parametrize(
    ('created_at', 'edited_at', 'expected'),
    (
        (datetime(2020, 4, 1), datetime(2020, 4, 2), TIMEZONE.localize(datetime(2020, 4, 2))),
        (None, datetime(2020, 4, 2), TIMEZONE.localize(datetime(2020, 4, 2))),
        (datetime(2020, 4, 1), None, TIMEZONE.localize(datetime(2020, 4, 1))),
        (None, None, None),
    ),
)
def test_get_display_date(mocker, created_at, edited_at, expected):
    # arrange & act
    result = get_display_date(created_at=created_at, edited_at=edited_at)

    # assert
    assert result == expected
