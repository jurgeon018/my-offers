from my_offers.entities.get_offers import AvailableActions
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Status


CAN_ARCHIVE_STATUSES = (Status.deactivated, Status.published, Status.draft)
CAN_DELETE_STATUSES = (Status.published, Status.draft, Status.blocked)


def get_available_actions(
        *,
        is_archived: bool,
        is_manual: bool,
        status: Status,
        can_update_edit_date: bool
) -> AvailableActions:
    return AvailableActions(
        can_update_edit_date=can_update_edit_date,
        can_move_to_archive=not is_archived and is_manual and status in CAN_ARCHIVE_STATUSES,
        can_delete=status in CAN_DELETE_STATUSES
    )
