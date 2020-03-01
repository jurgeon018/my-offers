from typing import Optional

from my_offers.repositories.monolith_cian_announcementapi.entities import Flags
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Status


def get_status(status: Optional[Status], flags: Optional[Flags]) -> Optional[str]:
    if flags and flags.is_archived:
        return 'В архиве'

    if not status:
        return None

    if status.is_published:
        return 'Опубликовано'

    if status.is_deleted:
        return 'Удалено'

    return None
