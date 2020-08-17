import pytest

from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import FlatType
from my_offers.services.similars.helpers.rooms_count import get_rooms_count


@pytest.mark.parametrize(
    ('rooms_count', 'rooms_for_sale_count', 'flat_type', 'expected'),
    (
        (1, 2, None, 1),
        (0, 2, None, 2),
        (0, 0, FlatType.open_plan, 1),
        (0, 0, FlatType.studio, 1),
        (0, 0, FlatType.rooms, None),
    ),
)
def test_get_rooms_count(rooms_count, rooms_for_sale_count, flat_type, expected):
    # arrange & act
    result = get_rooms_count(rooms_count=rooms_count, rooms_for_sale_count=rooms_for_sale_count, flat_type=flat_type)

    # assert
    assert result == expected
