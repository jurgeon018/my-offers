import pytest

from my_offers.entities.offer_view_model import AvailableActions
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Status
from my_offers.services.offer_view.fields import get_available_actions


@pytest.mark.parametrize('is_archived, is_manual, status, can_update_edit_date, expected', [
    (
        False, False, Status.deleted, False, AvailableActions(
            can_update_edit_date=False,
            can_move_to_archive=False,
            can_delete=False
        )
    ),
    (
        True, True, Status.published, True, AvailableActions(
            can_update_edit_date=True,
            can_move_to_archive=False,
            can_delete=True
        )
    ),
    (
        True, False, Status.published, True, AvailableActions(
            can_update_edit_date=True,
            can_move_to_archive=False,
            can_delete=True
        )
    ),
    (
        False, True, Status.published, True, AvailableActions(
            can_update_edit_date=True,
            can_move_to_archive=True,
            can_delete=True
        )
    ),
])
def test_get_features(is_archived, is_manual, status, can_update_edit_date, expected):
    # arrange & act
    result = get_available_actions(
        is_archived=is_archived,
        is_manual=is_manual,
        status=status,
        can_update_edit_date=can_update_edit_date,
    )

    # assert
    assert result == expected
