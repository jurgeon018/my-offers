from my_offers.helpers.status_tab import get_status_tab
from my_offers.repositories.monolith_cian_announcementapi.entities import Flags
from my_offers.repositories.monolith_cian_announcementapi.entities.flags import DraftReason
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Status as ObjectModelStatus
from my_offers.repositories.monolith_cian_ms_announcements.entities import ChangedAnnouncement
from my_offers.repositories.monolith_cian_ms_announcements.entities.changed_announcement import Status


STATUS_MAP = {
    Status.draft: ObjectModelStatus.draft,
    Status.published: ObjectModelStatus.published,
    Status.deactivated: ObjectModelStatus.deactivated,
    Status.refused: ObjectModelStatus.refused,
    Status.deleted: ObjectModelStatus.deleted,
    Status.sold: ObjectModelStatus.sold,
    Status.moderate: ObjectModelStatus.moderate,
    Status.removed_by_moderator: ObjectModelStatus.removed_by_moderator,
    Status.blocked: ObjectModelStatus.blocked,
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
