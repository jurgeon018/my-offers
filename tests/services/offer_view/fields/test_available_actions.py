import pytest

from my_offers.entities.get_offers import AvailableActions
from my_offers.repositories.agencies_settings.entities import AgencySettings
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Status
from my_offers.services.offer_view.fields import get_available_actions


@pytest.mark.parametrize('is_archived, is_manual, status, can_update_edit_date, expected', [
    (
        False, False, Status.deleted, False, AvailableActions(
            can_update_edit_date=False,
            can_move_to_archive=False,
            can_delete=False,
            can_edit=True,
            can_restore=False,
        )
    ),
    (
        True, True, Status.published, True, AvailableActions(
            can_update_edit_date=True,
            can_move_to_archive=False,
            can_delete=True,
            can_edit=True,
            can_restore=True,
        )
    ),
    (
        True, False, Status.published, True, AvailableActions(
            can_update_edit_date=False,
            can_move_to_archive=False,
            can_delete=False,
            can_edit=True,
            can_restore=False,
        )
    ),
    (
        False, True, Status.published, True, AvailableActions(
            can_update_edit_date=True,
            can_move_to_archive=True,
            can_delete=True,
            can_edit=True,
            can_restore=True,
        )
    ),
    (
        False, True, Status.published, True, AvailableActions(
            can_update_edit_date=True,
            can_move_to_archive=True,
            can_delete=True,
            can_edit=True,
            can_restore=True,
        )
    ),
])
def test_get_available_actions(is_archived, is_manual, status, can_update_edit_date, expected):
    # arrange & act
    result = get_available_actions(
        is_archived=is_archived,
        is_manual=is_manual,
        status=status,
        can_update_edit_date=can_update_edit_date,
        agency_settings=AgencySettings(
            can_sub_agents_edit_offers_from_xml=True,
            can_sub_agents_publish_offers=True,
            can_sub_agents_view_agency_balance=True,
            display_all_agency_offers=True,
        )
    )

    # assert
    assert result == expected


def test_get_available_actions__no_settings__actions():
    # arrange
    expected = AvailableActions(
        can_update_edit_date=False,
        can_move_to_archive=False,
        can_delete=False,
        can_edit=False,
        can_restore=False,
    )

    # act
    result = get_available_actions(
        is_archived=False,
        is_manual=False,
        status=Status.published,
        can_update_edit_date=False,
        agency_settings=None
    )

    # assert
    assert result == expected
