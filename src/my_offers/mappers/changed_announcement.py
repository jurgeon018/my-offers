from my_offers.helpers.status_tab import get_status_tab
from my_offers.repositories.monolith_cian_announcementapi.entities import Flags
from my_offers.repositories.monolith_cian_announcementapi.entities.flags import DraftReason
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Status
from my_offers.repositories.monolith_cian_ms_announcements.entities import ChangedAnnouncement


STATUS_MAP = {
    11: Status.draft,
    12: Status.published,
    14: Status.deactivated,
    15: Status.refused,
    16: Status.deleted,
    17: Status.sold,
    18: Status.moderate,
    19: Status.removed_by_moderator,
    20: Status.blocked,
}


def changed_announcement_map_from(changed_announcement: ChangedAnnouncement):
    if changed_announcement.flags:
        flags = Flags()
        if changed_announcement.flags & 1:
            flags.is_archived = True
        if changed_announcement.flags & 2:
            flags.draft_reason = DraftReason.ready_for_upload_delete
    else:
        flags = None

    return {
            'offer_id': changed_announcement.id,
            'status_tab': get_status_tab(
                offer_flags=flags,
                offer_status=STATUS_MAP.get(changed_announcement.status, Status.deleted),
            ).value,
            'row_version': changed_announcement.row_version,
        }
