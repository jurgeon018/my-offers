from datetime import datetime, timedelta
from typing import Optional

from cian_helpers.timezone import is_aware, make_aware
from pytils.numeral import choose_plural


def get_left_time_display(*, current: datetime, end: datetime) -> str:
    if end < current:
        raise ValueError('Дата окончания меньше даты начала')

    delta: timedelta = end - current

    if delta.days > 0:
        value = delta.days
        units = ('день', 'дня', 'дней')
    elif delta.seconds > 60 * 60:
        value = int(delta.seconds / (60 * 60))
        units = ('час', 'часа', 'часов')
    else:
        return 'менее 1 часа'

    return '{} {}'.format(value, choose_plural(value, units))


def get_aware_date(date: Optional[datetime]) -> Optional[datetime]:
    if not date:
        return None

    if is_aware(date):
        return date

    return make_aware(date)
