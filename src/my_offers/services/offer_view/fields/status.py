from typing import Optional

from my_offers.repositories.monolith_cian_announcementapi.entities import Flags
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Status


def get_status(is_archived: bool, status: Optional[Status]) -> Optional[str]:
    if is_archived:
        return 'В архиве'

    if not status:
        return None

    if status.is_published:
        return 'Опубликовано'

    if status.is_deleted:
        return 'Удалено'

    return None
