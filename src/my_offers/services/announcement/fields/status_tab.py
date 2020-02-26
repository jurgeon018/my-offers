from my_offers import enums
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

    Status.deleted: enums.OfferStatusTab.deleted,
}


def get_status_tab(*, is_archived: bool, offer_status: Status) -> enums.OfferStatusTab:
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
    if is_archived:
        return enums.OfferStatusTab.archived

    return STATUS_TO_TAB_MAP[offer_status]
