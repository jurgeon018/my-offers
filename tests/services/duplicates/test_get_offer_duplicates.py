import pytest

from my_offers.helpers.similar import is_offer_for_similar
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category, Status


@pytest.mark.parametrize(
    ('status', 'category', 'expected'),
    (
        (Status.deactivated, Category.flat_sale, False),
        (Status.published, Category.flat_sale, True),
        (Status.published, Category.daily_flat_rent, False),
    )
)
def test_is_offer_for_similar(status, category, expected):
    # arrange & act
    result = is_offer_for_similar(status=status, category=category)

    # assert
    assert result == expected
