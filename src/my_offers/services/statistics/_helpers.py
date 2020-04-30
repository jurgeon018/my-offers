from collections import defaultdict
from datetime import datetime
from typing import Any, Iterable, List, Tuple

from cassandra import ConsistencyLevel
from cassandra.query import PreparedStatement  # pylint: disable=no-name-in-module
from cian_cassandra.sessions import CassandraClient
from dateutil.rrule import MONTHLY, rrule
from simple_settings import settings


async def cassandra_execute(
        alias: str,
        stmt: PreparedStatement,
        params: Iterable[Any] = None,
        consistency_level: int = ConsistencyLevel.LOCAL_QUORUM,
        timeout: float = None
) -> List[Any]:
    params = params or []
    timeout = timeout or float(settings.CASSANDRA_DEFAULT_TIMEOUT)
    stmt = stmt.bind(params)  # type: ignore
    stmt.consistency_level = consistency_level
    return await CassandraClient.execute(stmt, timeout=timeout, alias=alias)


def get_months_intervals(date_from: datetime, date_to: datetime) -> List[Tuple[datetime, datetime]]:
    """ Монолитная функция получения интервалов по месяцам (см. тесты).

        Перенесена как есть со всеми тестами.
    """

    if date_from == date_to:
        return [(date_from, date_to)]

    month_range = list(rrule(freq=MONTHLY, dtstart=date_from, until=date_to, bymonthday=[1, -1]))
    month_range = [date_from] + month_range + [date_to]

    dates_by_months = defaultdict(list)
    for d in month_range:
        dates_by_months[(d.year, d.month)].append(d)

    months_intervals = []
    for _, dates in sorted(dates_by_months.items()):
        months_intervals.append((min(dates), max(dates)))

    return months_intervals
