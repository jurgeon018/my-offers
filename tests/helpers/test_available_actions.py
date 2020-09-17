import pytest
from simple_settings.utils import settings_stub

from my_offers.entities.available_actions import AvailableActions
from my_offers.enums import OfferPayedBy
from my_offers.helpers import get_available_actions
from my_offers.helpers.available_actions import _can_raise, _can_restore
from my_offers.repositories.agencies_settings.entities import AgencySettings
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Status


@pytest.mark.parametrize('is_master_agent, is_archived, is_manual, payed_by, status, can_update_edit_date, expected', [
    (
        True, False, False, None, Status.deleted, False, AvailableActions(
            can_update_edit_date=False,
            can_move_to_archive=False,
            can_delete=False,
            can_edit=True,
            can_restore=False,
            can_raise=False,
            can_change_publisher=False,
            can_view_similar_offers=False
        )
    ),
    (
        True, True, True, None, Status.published, True, AvailableActions(
            can_update_edit_date=False,
            can_move_to_archive=False,
            can_delete=True,
            can_edit=False,
            can_restore=True,
            can_raise=False,
            can_change_publisher=True,
            can_view_similar_offers=False
        )
    ),
    (
        True, True, False, None, Status.published, True, AvailableActions(
            can_edit=False,
            can_restore=False,
            can_update_edit_date=False,
            can_move_to_archive=False,
            can_delete=False,
            can_raise=False,
            can_change_publisher=False,
            can_view_similar_offers=False
        )
    ),
    (
        True, False, True, None, Status.published, True, AvailableActions(
            can_update_edit_date=True,
            can_move_to_archive=True,
            can_delete=True,
            can_edit=True,
            can_restore=False,
            can_raise=True,
            can_change_publisher=True,
            can_view_similar_offers=False
        )
    ),
    (
        False, False, True, None, Status.published, True, AvailableActions(
            can_update_edit_date=True,
            can_move_to_archive=True,
            can_delete=True,
            can_edit=True,
            can_restore=False,
            can_raise=True,
            can_change_publisher=False,
            can_view_similar_offers=False
        )
    ),
    (
        True, False, True, OfferPayedBy.by_master, Status.published, True, AvailableActions(
            can_update_edit_date=True,
            can_move_to_archive=True,
            can_delete=True,
            can_edit=True,
            can_restore=False,
            can_raise=True,
            can_change_publisher=True,
            can_view_similar_offers=False
        )
    ),
    (
        False, False, True, OfferPayedBy.by_master, Status.published, True, AvailableActions(
            can_update_edit_date=True,
            can_move_to_archive=True,
            can_delete=True,
            can_edit=True,
            can_restore=False,
            can_raise=True,
            can_change_publisher=False,
            can_view_similar_offers=False
        )
    ),
    (
        False, False, True, OfferPayedBy.by_agent, Status.published, True, AvailableActions(
            can_update_edit_date=True,
            can_move_to_archive=True,
            can_delete=True,
            can_edit=True,
            can_restore=False,
            can_raise=True,
            can_change_publisher=False,
            can_view_similar_offers=False
        )
    ),
])
def test_get_available_actions(is_master_agent, is_archived, is_manual, payed_by, status, can_update_edit_date, expected):
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
        ),
        is_in_hidden_base=False,
        is_master_agent=is_master_agent,
        force_raise=False,
        payed_by=payed_by
    )

    # assert
    assert result == expected


@pytest.mark.parametrize('is_master_agent, is_archived, is_manual, payed_by, status, can_update_edit_date, expected', [
     (
        True, False, True, OfferPayedBy.by_agent, Status.published, True, AvailableActions(
            can_update_edit_date=False,
            can_move_to_archive=False,
            can_delete=False,
            can_edit=False,
            can_restore=False,
            can_raise=False,
            can_change_publisher=False,
            can_view_similar_offers=False
        )
        ),
])
def test_get_available_actions_for_agent_offer_payed_by_agent(is_master_agent, is_archived, is_manual, payed_by, status, can_update_edit_date, expected):
    # arrange & act
    with settings_stub(MASTER_CAN_SEE_AGENT_PAYED_OFFERS=True):
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
            ),
            is_in_hidden_base=False,
            is_master_agent=is_master_agent,
            force_raise=False,
            payed_by=payed_by
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
        can_raise=False,
        can_change_publisher=False,
        can_view_similar_offers=False
    )

    # act
    result = get_available_actions(
        is_archived=False,
        is_manual=False,
        status=Status.published,
        can_update_edit_date=False,
        agency_settings=None,
        is_in_hidden_base=False,
        is_master_agent=False,
        force_raise=False
    )

    # assert
    assert result == expected


@pytest.mark.parametrize(
    ('is_removed_by_moderator', 'is_archived', 'is_discontinued', 'expected'),
    (
        (False, False, False, False),
        (True, False, False, False),
        (False, True, False, True),
        (True, True, False, False),
        (False, False, True, True),
    )
)
def test__can_restore(mocker, is_archived, is_removed_by_moderator, is_discontinued, expected):
    # arrange & act
    result = _can_restore(
        is_archived=is_archived,
        is_removed_by_moderator=is_removed_by_moderator,
        is_discontinued=is_discontinued
    )

    # assert
    assert result == expected


@pytest.mark.parametrize(
    ('force_raise', 'is_in_hidden_base', 'is_published', 'is_archived', 'expected'),
    (
        (False, True, False, False, False),
        (False, False, True, False, True),
        (False, True, True, False, False),
        (False, False, False, True, False),
        (False, False, False, False, False),
        (True, False, False, False, True),
    )
)
def test__can_raise(mocker, force_raise, is_archived, is_published, is_in_hidden_base, expected):
    # arrange & act
    result = _can_raise(
        force_raise=force_raise,
        is_archived=is_archived,
        is_published=is_published,
        is_in_hidden_base=is_in_hidden_base,
    )

    # assert
    assert result == expected
