import pytest

from my_offers.entities import Coverage, Statistics
from my_offers.services.offer_view.fields.statistics import get_statistics


@pytest.mark.parametrize(
    ('views', 'searches', 'favorites', 'expected'),
    (
        (10, 20, 30, Statistics(views=10, shows=20, favorites=30)),
        (None, None, None, Statistics(views=None, shows=None, favorites=None)),
    )
)
def test_get_statistics(views, searches, favorites, expected):
    # arrange & act
    result = get_statistics(searches=searches, views=views, favorites=favorites)

    # assert
    assert result == expected
