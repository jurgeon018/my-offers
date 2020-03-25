from typing import Optional

from my_offers import entities
from my_offers.repositories.agencies_settings.entities import AgencySettings
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Status


CAN_ARCHIVE_STATUSES = (Status.deactivated, Status.published, Status.draft)
CAN_DELETE_STATUSES = (Status.published, Status.draft, Status.blocked)


def get_available_actions(
        *,
        is_archived: bool,
        is_manual: bool,
        status: Status,
        can_update_edit_date: bool,
        agency_settings: Optional[AgencySettings],
) -> entities.AvailableActions:
    if not is_manual:
        return entities.AvailableActions(
            can_edit=agency_settings.can_sub_agents_edit_offers_from_xml if agency_settings else False,
            can_delete=False,
            can_restore=False,
            can_update_edit_date=False,
            can_move_to_archive=False,
        )

    return entities.AvailableActions(
        can_edit=True,
        can_delete=status in CAN_DELETE_STATUSES,
        can_restore=True,
        can_update_edit_date=can_update_edit_date,
        can_move_to_archive=not is_archived and status in CAN_ARCHIVE_STATUSES,
    )
