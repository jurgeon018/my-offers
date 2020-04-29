import time
from datetime import datetime

from cian_cassandra.statement import CassandraStatement

from my_offers.services.statistics._helpers import cassandra_execute


stmts = CassandraStatement('statistics')
stmts.select_completed_total_date = """
SELECT
    day, month, year
FROM
    statistics.completed_total
WHERE
    id = ?
"""


class StatisticCompletedDateNotAvailable(Exception):
    pass


class BaseStatCassandraRepository:
    KEYSPACE = 'statistics'
    COMPLETED_TOTAL_ID = -1
    COMPLETED_DATE_CACHE_TTL = 5 * 60
    _cached_completed_date = None
    _last_update_completed_date = None

    async def _get_completed_date(self) -> datetime:
        result = await cassandra_execute(
            alias=self.KEYSPACE,
            params=[self.COMPLETED_TOTAL_ID],
            stmt=stmts.select_completed_total_date,
        )

        if not result:
            raise StatisticCompletedDateNotAvailable

        return datetime(result[0].year, result[0].month, result[0].day)

    async def get_completed_date(self) -> datetime:
        now = time.time()
        if (
                self._cached_completed_date is None or
                self._last_update_completed_date is None or
                now - self._last_update_completed_date > self.COMPLETED_DATE_CACHE_TTL
        ):
            self._cached_completed_date = await self._get_completed_date()
            self._last_update_completed_date = now

        return self._cached_completed_date
