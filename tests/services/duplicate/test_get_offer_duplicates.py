import pytest

from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category, Status
from my_offers.services.duplicates._get_offer_duplicates import validate_offer


@pytest.mark.parametrize(
    ('status', 'category', 'expected'),
    (
        (Status.deactivated, Category.flat_sale, False),
        (Status.published, Category.flat_sale, True),
        (Status.published, Category.daily_flat_rent, False),
    )
)
def test_validate_offer(status, category, expected):
    # arrange & act
    result = validate_offer(status=status, category=category)

    # assert
    assert result == expected
