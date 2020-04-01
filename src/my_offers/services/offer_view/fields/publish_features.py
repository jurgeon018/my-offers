from datetime import timedelta
from typing import List, Optional

from my_offers.repositories.monolith_cian_announcementapi.entities import PublishTerms
from my_offers.services.offer_view.fields.autoprolong import is_autoprolong


def get_publish_features(publish_terms: Optional[PublishTerms], payed_remain: Optional[timedelta]) -> List[str]:
    if payed_remain and payed_remain.days > 365:
        return ['бессрочно']

    result = []
    if payed_remain:
        result.append('Осталось {}'.format(_get_remain(payed_remain)))

    if is_autoprolong(publish_terms=publish_terms):
        result.append('автопродление')

    return result


def _get_remain(delta: timedelta):
    if delta.days > 0:
        return '{} д.'.format(delta.days)

    if delta.seconds > 60 * 60:
        return '{} ч.'.format(delta.seconds // (60 * 60))

    return ' {} м.'.format(delta.seconds // 60)
