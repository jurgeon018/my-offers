import pytest

from my_offers.enums.offer_status import OfferStatus
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Status
from my_offers.services.offer_view.fields.status import get_status, get_status_type


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


@pytest.mark.parametrize(
    ('status', 'is_manual', 'expected'),
    (
        (None, True, None),
        (None, False, OfferStatus.xml),
        (Status.draft, True, OfferStatus.draft),
        (Status.draft, False, OfferStatus.xml),
        (Status.published, False, OfferStatus.xml),
        (Status.published, True, None),
    )
)
def test_get_status_type(mocker, status, is_manual, expected):
    # arrange & act
    result = get_status_type(status=status, is_manual=is_manual)

    # assert
    assert result == expected
