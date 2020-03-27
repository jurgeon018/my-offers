from datetime import datetime, timedelta
from typing import Optional

import pytz
from cian_helpers import date_time, timezone
from simple_settings import settings

from my_offers.entities.get_offers import NotActiveInfo
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
        edit_date: Optional[datetime] = None,
        on_premoderation: Optional[bool] = False,
) -> Optional[NotActiveInfo]:
    if on_premoderation:
        return NotActiveInfo(
            status='На модерации',
            message='Объявление будет автоматически опубликовано после проверки модератором'
        )

    if import_error:
        return NotActiveInfo(status='Ошибка импорта', message=import_error)

    if not status or status.is_published:
        return None

    if status.is_draft:
        return NotActiveInfo(status='Черновик')

    if status in STATUSES_FOR_ARCHIVATION:
        message: Optional[str] = None

        if edit_date:
            now = datetime.now(tz=pytz.UTC)
            if timezone.is_naive(edit_date):
                edit_date = date_time.localize(edit_date)

            archive_date = edit_date + timedelta(days=settings.DAYS_BEFORE_ARCHIVATION)  # type: ignore[operator]
            if archive_date > now:  # type: ignore[operator]
                message = 'До автоматического удаления осталось {}'.format(
                    get_left_time_display(current=now, end=archive_date)
                )

        return NotActiveInfo(
            status='Снято с публикации',
            message=message
        )

    return None
