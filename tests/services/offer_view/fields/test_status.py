import pytest

from my_offers.repositories.monolith_cian_announcementapi.entities import Flags
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Status
from my_offers.services.offer_view.fields.status import get_status


@pytest.mark.parametrize(
    ('status', 'flags', 'expected'),
    (
        (None, None, None),
        (None, Flags(is_archived=True), 'В архиве'),
        (Status.published, Flags(is_archived=True), 'В архиве'),
        (Status.published, Flags(is_archived=False), 'Опубликовано'),
        (Status.deleted, Flags(is_archived=False), 'Удалено'),
        (Status.sold, Flags(is_archived=False), None),
    )
)
def test_get_status(mocker, status, flags, expected):
    # arrange & act
    result = get_status(status=status, flags=flags)

    # assert
    assert result == expected
