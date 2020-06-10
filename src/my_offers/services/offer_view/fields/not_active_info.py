from datetime import datetime, timedelta
from typing import Optional

import pytz
from cian_helpers import date_time, timezone
from simple_settings import settings

from my_offers.entities.get_offers import NotActiveInfo
from my_offers.enums.not_active_status import NotActiveStatus
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Status
from my_offers.services.offer_view.helpers.time import get_left_time_display


STATUSES_FOR_ARCHIVATION = {
    Status.deactivated,
    Status.deleted,
    Status.removed_by_moderator,
    Status.refused,
    Status.sold,
    Status.moderate,
    Status.blocked,
}


def get_not_active_info(
        *,
        status: Optional[Status],
        import_error: Optional[str] = None,
        archive_date: Optional[datetime] = None,
        on_premoderation: Optional[bool] = False,
) -> Optional[NotActiveInfo]:
    if on_premoderation:
        return NotActiveInfo(
            status='На модерации',
            message='Объявление будет автоматически опубликовано после проверки модератором',
            status_type=NotActiveStatus.premoderation
        )

    if import_error:
        return NotActiveInfo(
            status='Ошибка импорта',
            message=import_error,
            status_type=NotActiveStatus.import_error
        )

    if not status or status.is_published:
        return None

    if status.is_draft:
        return NotActiveInfo(status='Черновик', status_type=NotActiveStatus.discontinued)

    if status in STATUSES_FOR_ARCHIVATION:
        message: Optional[str] = None

        if archive_date:
            now = datetime.now(tz=pytz.UTC)
            if archive_date > now:
                # обсуждение: https://cianru.slack.com/archives/CNYSG64UD/p1585559101117800
                message = 'Будет автоматически перенесено в архив через {}'.format(
                    get_left_time_display(current=now, end=archive_date)
                )

        return NotActiveInfo(
            status='Снято с публикации',
            message=message,
            status_type=NotActiveStatus.discontinued
        )

    return None
