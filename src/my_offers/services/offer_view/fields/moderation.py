from typing import Optional

from my_offers.entities.get_offers import Moderation
from my_offers.entities.moderation import OfferOffence
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Status


MODERATION_STATUS_MAPPING = {
    Status.refused: 'Отклонено модератором',
    Status.removed_by_moderator: 'Удалено модератором',
    Status.blocked: 'Заблокировано'
}

DECLINED_STATUS = [
    Status.blocked,
    Status.removed_by_moderator,
    Status.refused,
]


def get_moderation(*, status: Optional[Status], offer_offence: Optional[OfferOffence]) -> Optional[Moderation]:
    if not status or status not in DECLINED_STATUS:
        return None

    if status.is_blocked:
        # TODO: https://jira.cian.tech/browse/CD-75832
        return Moderation(
            declined_date=None,
            can_delete=False,
            can_move_to_archive=False,
            is_declined=False,
            offence_status=MODERATION_STATUS_MAPPING[status]
        )

    if not offer_offence:
        return None

    if offer_offence.offence_status.is_corrected:
        return None

    moderation = Moderation(
        declined_date=offer_offence.created_date,
        can_delete=False,
        can_move_to_archive=False,
        reason=offer_offence.offence_text,
        is_declined=status.is_refused,
        offence_status=MODERATION_STATUS_MAPPING[status]
    )

    return moderation
