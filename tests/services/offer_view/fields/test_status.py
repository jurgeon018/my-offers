import pytest

from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Status
from my_offers.services.offer_view.fields.status import get_status


@pytest.mark.parametrize(
    ('status', 'is_archived', 'expected'),
    (
        (None, False, None),
        (None, True, 'В архиве'),
        (Status.published, True, 'В архиве'),
        (Status.published, False, 'Опубликовано'),
        (Status.deleted, False, 'Удалено'),
        (Status.sold, False, None),
    )
)
def test_get_status(mocker, status, is_archived, expected):
    # arrange & act
    result = get_status(status=status, is_archived=is_archived)

    # assert
    assert result == expected
