from typing import Optional

from my_offers import enums
from my_offers.helpers.fields import is_archived
from my_offers.repositories.monolith_cian_announcementapi.entities import Flags
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Status


STATUS_TO_TAB_MAP = {
    Status.published: enums.OfferStatusTab.active,

    Status.draft: enums.OfferStatusTab.not_active,
    Status.deactivated: enums.OfferStatusTab.not_active,
    Status.sold: enums.OfferStatusTab.not_active,

    Status.refused: enums.OfferStatusTab.declined,
    Status.moderate: enums.OfferStatusTab.declined,
    Status.removed_by_moderator: enums.OfferStatusTab.declined,
    Status.blocked: enums.OfferStatusTab.declined,
}


def get_status_tab(*, offer_flags: Optional[Flags], offer_status: Status) -> enums.OfferStatusTab:
    # Логика работы вкладок
    # -- вкладка активные
    # 'published',
    # -- вкладка неактивные
    # 'draft',
    # 'deactivated',
    # 'sold',
    # -- вкладка отклоненные
    # 'refused',
    # 'moderate',
    # 'removed_by_moderator',
    # 'blocked',
    # -- вкладка архивные
    # флаг из isArchived
    # -- Удаленные
    # 'deleted'
    if offer_status.is_deleted:
        return enums.OfferStatusTab.deleted

    if offer_flags and offer_flags.draft_reason and offer_flags.draft_reason.is_ready_for_upload_delete:
        return enums.OfferStatusTab.deleted

    if is_archived(offer_flags):
        return enums.OfferStatusTab.archived

    return STATUS_TO_TAB_MAP[offer_status]
