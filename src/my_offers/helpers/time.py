from datetime import datetime, timedelta

from pytils.numeral import choose_plural


def get_left_time_display(*, current: datetime, end: datetime):
    delta: timedelta = end - current

    if delta.days > 0:
        value = delta.days
        units = ('день', 'дня', 'дней')
    elif delta.seconds > 60 * 60:
        value = int(delta.seconds / 60 * 60)
        units = ('час', 'часа', 'часов')
    else:
        return 'менее 1 часа'

    return '{} {}'.format(value, choose_plural(value, units))
