import itertools
from datetime import datetime, time, timedelta
from typing import Dict, List

import pytz
from cian_core.runtime_settings import runtime_settings
from tornado import gen

from my_offers.services.statistics._cassandra_statistics import (
    base_cs_repo,
    coverage_cs_repo,
    search_coverage_cs_repo,
    views_cs_repo,
)
from my_offers.services.statistics._helpers import get_months_intervals


# TODO: https://jira.cian.tech/browse/CD-80277
#   Этот код запрещено использовать внутри микросервиса! (исключения: /public/v2/get-offers/, /v2/get-offers/)
#   Подробности в задаче CD-80277


async def get_favorites_counts(offer_ids: List[int]) -> Dict[int, int]:
    """
        Получить кол-во избранного по объявлениям.
        Примечание: монолит не умеет получать избранное по диапазону дат.

        Это порт вызова `get_offers_daily_coverage.main(...)`
        https://bitbucket.org/cianmedia/cian/src/4b50768fa34f87ecaca5f35966c48cd442e43b79/cian/statistics/services.py#lines-52
    """
    today = datetime.now(pytz.utc)
    completed_date = await base_cs_repo.get_completed_date()

    offer_coverages_total, offer_coverages_current = await gen.multi([
        coverage_cs_repo.get_offers_coverage_total(
            offers_ids=offer_ids,
            date_from=completed_date.date(),
            date_to=completed_date.date(),
        ),
        coverage_cs_repo.get_offers_coverage_current(
            offers_ids=offer_ids,
            date_from=(completed_date + timedelta(days=1)).date(),
            date_to=today.date(),
        ),
    ])

    chained_stats = itertools.chain.from_iterable([offer_coverages_total, offer_coverages_current])
    favorites = dict.fromkeys(offer_ids, 0)

    for item in chained_stats:
        favorites[item.offer_id] += item.favorite_added or 0

    return favorites


async def get_searches_counts(offer_ids: List[int], date_from: datetime, date_to: datetime) -> Dict[int, int]:
    """
        Получить количесво просмотров для объявлений.

        Порт функции из монолита
        https://bitbucket.org/cianmedia/cian/src/4b50768fa34f87ecaca5f35966c48cd442e43b79/cian/search_coverage/services/get_offers_daily_coverage/service.py#lines-17
    """
    completed_date = await base_cs_repo.get_completed_date()

    futures = {
        'daily': coverage_cs_repo.get_offers_coverage_daily(
            offers_ids=offer_ids,
            date_from=date_from.date(),
            date_to=completed_date.date(),
        ),
        'current': coverage_cs_repo.get_offers_coverage_current(
            offers_ids=offer_ids,
            date_from=(completed_date + timedelta(days=1)).date(),
            date_to=date_to.date(),
        )
    }

    if new_table_date_from_str := runtime_settings.get('SEARCH_COVERAGE_NEW_TABLE_DATE_FROM', None):
        new_table_date_from = datetime.strptime(new_table_date_from_str, '%Y-%m-%d').date()
        if new_table_date_from <= date_to.date():
            futures['v2'] = search_coverage_cs_repo.get_offers_counters(
                offers_ids=offer_ids,
                date_from=new_table_date_from,
                date_to=date_to.date(),
            )

    repo_results = await gen.multi(futures)
    chained_stats = repo_results['daily'] + repo_results['current']

    offers_dict = dict.fromkeys(offer_ids, 0)

    for row in chained_stats:
        offers_dict[row.offer_id] += row.searches_count or 0

    for v2_row in repo_results.get('v2', []):
        offers_dict[v2_row.offer_id] += v2_row.searches_count or 0

    return offers_dict


async def get_views_counts(offer_ids: List[int], date_from: datetime, date_to: datetime) -> Dict[int, int]:
    """
        Получить количесво попаданий в выдачу для объявлений.

        Порт функции из монолита
        https://bitbucket.org/cianmedia/cian/src/4b50768fa34f87ecaca5f35966c48cd442e43b79/cian/search_coverage/services/get_offer_periods_stats_desktop/service.py#lines-21
    """
    completed_date = await base_cs_repo.get_completed_date()

    futures = {
        offer_id: _get_views_by_date_range(
            offer_id=offer_id,
            date_from=date_from,
            date_to=date_to,
            completed_date=completed_date
        )
        for offer_id in offer_ids
    }

    return await gen.multi(futures)  # type: ignore


async def _get_views_by_date_range(
        offer_id: int,
        date_from: datetime,
        date_to: datetime,
        completed_date: datetime,
) -> int:
    # views_daily stat
    intervals = get_months_intervals(date_from=datetime.combine(date_from, time.min), date_to=completed_date)
    views_daily_futures = []
    for start_interval, end_interval in intervals:
        views_daily_futures.append(
            views_cs_repo.get_views_daily(
                offer_id=offer_id,
                year=start_interval.year,
                month=start_interval.month,
                day_from=start_interval.day,
                day_to=end_interval.day,
            )
        )

    # views_current stat
    delta = date_to.date() - completed_date.date()
    views_current_futures = []
    if delta.days > 0:
        intervals = get_months_intervals(
            date_from=completed_date + timedelta(days=1),
            date_to=datetime.combine(date_to, time.min)
        )
        for start_interval, end_interval in intervals:
            views_current_futures.append(
                views_cs_repo.get_views_current(
                    offer_id=offer_id,
                    year=start_interval.year,
                    month=start_interval.month,
                    day_from=start_interval.day,
                    day_to=end_interval.day,
                )
            )

    # Fetch all stats
    offer_stats = await gen.multi({
        'views_daily': views_daily_futures,
        'views_current': views_current_futures,
    })

    views_daily_rows = list(itertools.chain.from_iterable(offer_stats['views_daily']))
    views_current_rows = list(itertools.chain.from_iterable(offer_stats['views_current']))
    daily_stats = views_daily_rows + views_current_rows

    return sum(s.views for s in daily_stats)
