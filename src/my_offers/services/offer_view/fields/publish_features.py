from datetime import timedelta
from typing import List, Optional

from my_offers.repositories.monolith_cian_announcementapi.entities import PublishTerms
from my_offers.services.offer_view.helpers.terms import is_daily_charge


def get_publish_features(publish_terms: Optional[PublishTerms], payed_remain: Optional[timedelta]) -> List[str]:
    if payed_remain and payed_remain.days > 365:
        return ['бессрочно']

    if not publish_terms:
        return []

    if is_daily_charge(publish_terms.terms):
        return []

    result = []
    if payed_remain:
        result.append('осталось {}'.format(_get_remain(payed_remain)))
    if publish_terms.autoprolong:
        result.append('автопродление')

    return result


def _get_remain(delta: timedelta):
    if delta.days > 0:
        return '{} д.'.format(delta.days)

    if delta.seconds > 60 * 60:
        return '{} ч.'.format(delta.seconds // (60 * 60))

    return '{} м.'.format(delta.seconds // 60)
