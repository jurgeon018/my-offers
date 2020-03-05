from datetime import datetime

import pytz
from typing import Optional

from my_offers.entities.get_offers import NotActiveInfo
from my_offers.helpers.time import get_left_time_display
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Status


def get_not_active_info(
        *,
        status: Status,
        import_error: str,
        archive_date: Optional[datetime] = None
) -> NotActiveInfo:
    if import_error:
        return NotActiveInfo(status='Ошибка импорта', message=import_error)

    if status.is_draft:
        return NotActiveInfo(status='Черновик')

    if status.is_deactivated:
        now = datetime.now(tz=pytz.UTC)
        if archive_date and archive_date > now:
            message = 'До автоматического удаления осталось {}'.format(
                get_left_time_display(current=now, end=archive_date)
            )
        else:
            message = None
        return NotActiveInfo(
            status='Снято с публикации',
            message=message
        )
