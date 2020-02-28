import pytest

from my_offers.enums import OfferStatusTab
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Status
from my_offers.services.announcement.fields.status_tab import get_status_tab


@pytest.mark.parametrize(
    ('is_archived', 'offer_status', 'expected'),
    (
        (True, Status.draft, OfferStatusTab.archived),
        (False, Status.draft, OfferStatusTab.not_active),
        (False, Status.published, OfferStatusTab.active),
        (False, Status.deactivated, OfferStatusTab.not_active),
        (False, Status.refused, OfferStatusTab.declined),
        (False, Status.deleted, OfferStatusTab.deleted),
        (False, Status.sold, OfferStatusTab.not_active),
        (False, Status.moderate, OfferStatusTab.declined),
        (False, Status.removed_by_moderator, OfferStatusTab.declined),
        (False, Status.blocked, OfferStatusTab.declined),
    )
)
def test_get_status_tab(mocker, is_archived, offer_status, expected):
    # arrange & act
    result = get_status_tab(is_archived=is_archived, offer_status=offer_status)

    # assert
    assert result == expected
