import pytest

from my_offers.enums import OfferStatusTab
from my_offers.helpers.status_tab import get_status_tab
from my_offers.repositories.monolith_cian_announcementapi.entities import Flags
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Status


@pytest.mark.parametrize(
    ('flags', 'offer_status', 'expected'),
    (
        (Flags(is_archived=True), Status.draft, OfferStatusTab.archived),
        (Flags(is_archived=None), Status.draft, OfferStatusTab.not_active),
        (Flags(is_archived=False), Status.published, OfferStatusTab.active),
        (Flags(is_archived=False), Status.deactivated, OfferStatusTab.not_active),
        (Flags(is_archived=False), Status.refused, OfferStatusTab.declined),
        (Flags(is_archived=False), Status.deleted, OfferStatusTab.deleted),
        (Flags(is_archived=False), Status.sold, OfferStatusTab.not_active),
        (Flags(is_archived=False), Status.moderate, OfferStatusTab.declined),
        (Flags(is_archived=False), Status.removed_by_moderator, OfferStatusTab.declined),
        (Flags(is_archived=False), Status.blocked, OfferStatusTab.declined),
    )
)
def test_get_status_tab(mocker, flags, offer_status, expected):
    # arrange & act
    result = get_status_tab(offer_flags=flags, offer_status=offer_status)

    # assert
    assert result == expected
