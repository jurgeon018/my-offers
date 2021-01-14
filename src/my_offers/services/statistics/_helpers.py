import operator
from collections import defaultdict
from datetime import datetime
from functools import reduce
from typing import Any, Iterable, List, Tuple

from cassandra import ConsistencyLevel
from cassandra.query import PreparedStatement  # pylint: disable=no-name-in-module
from cian_cassandra.sessions import CassandraClient
from dateutil.rrule import MONTHLY, rrule
from simple_settings import settings
from tornado import gen


async def cassandra_execute(
        alias: str,
        stmt: PreparedStatement,
        params: Iterable[Any] = None,
        consistency_level: int = ConsistencyLevel.LOCAL_QUORUM,
        timeout: float = None
) -> List[Any]:

    params = params or []
    timeout = timeout or float(settings.CASSANDRA_DEFAULT_TIMEOUT)
    statement = stmt.bind(params)
    statement.consistency_level = consistency_level
    return await CassandraClient.execute(statement, timeout=timeout, alias=alias)


async def cassandra_execute_grouped(
        alias: str,
        keyspace: str,
        stmt: PreparedStatement,
        table: str,
        keys: Iterable[Any] = None,
        params: Iterable[Any] = None,
        consistency_level: int = ConsistencyLevel.LOCAL_QUORUM,
        timeout: float = None
) -> List[Any]:
    partition_keys_groups = CassandraClient.group_keys_by_replica(
        keyspace=keyspace,
        table=table,
        keys=[(offer_id,) for offer_id in keys],  # type: ignore
    )

    results = await gen.multi([
        cassandra_execute(
            alias=alias,
            stmt=stmt,
            params=[[keys[0] for keys in keys], *params],  # type: ignore
            consistency_level=consistency_level,
            timeout=timeout
        )
        for keys in partition_keys_groups
    ])

    return reduce(operator.add, results, [])


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
