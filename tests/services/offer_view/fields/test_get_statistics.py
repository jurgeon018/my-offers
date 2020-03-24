import pytest

from my_offers.entities import Coverage, Statistics
from my_offers.services.offer_view.fields.statistics import get_statistics


@pytest.mark.parametrize(
    ('coverage', 'favorites', 'expected'),
    (
        (Coverage(searches_count=10, shows_count=20, coverage=50), 20, Statistics(views=10, shows=20, favorites=20)),
        (None, 20, Statistics(views=None, shows=None, favorites=20)),
    )
)
def test_get_statistics(coverage, favorites, expected):
    # arrange & act
    result = get_statistics(coverage=coverage, favorites=favorites)

    # assert
    assert result == expected
