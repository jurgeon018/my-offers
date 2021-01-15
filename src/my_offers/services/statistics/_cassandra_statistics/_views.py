from dataclasses import dataclass
from typing import List

from cian_cassandra.statement import CassandraStatement
from cian_entities import EntityMapper

from my_offers.services.statistics._helpers import cassandra_execute


stmts = CassandraStatement('statistics')

stmts.select_views_daily_days_range = """
SELECT
    offer_id, views
FROM
  statistics.views_daily
WHERE
  offer_id = ?
  AND year = ?
  AND month = ?
  AND day >= ?
  AND day <= ?
"""

stmts.select_views_current_days_range = """
SELECT
   offer_id, views
FROM
  statistics.views_current
WHERE
  offer_id = ?
  AND year = ?
  AND month = ?
  AND day >= ?
  AND day <= ?
"""


@dataclass
class ViewsRow:
    offer_id: int
    views: int


_search_coverage_counters_row_mapper = EntityMapper(
    entity=ViewsRow,
    without_camelcase=True,
)


class ViewsCassandraRepository:
    KEYSPACE = 'statistics'

    async def get_views_daily(self, offer_id: int, year: int, month: int, day_from: int, day_to: int) -> List[ViewsRow]:
        rows = await cassandra_execute(
            alias=self.KEYSPACE,
            stmt=stmts.select_views_daily_days_range,
            params=[offer_id, year, month, day_from, day_to]
        )

        return [_search_coverage_counters_row_mapper.map_from(row._asdict()) for row in rows]

    async def get_views_current(
            self,
            offer_id: int,
            year: int,
            month: int,
            day_from: int,
            day_to: int
    ) -> List[ViewsRow]:
        rows = await cassandra_execute(
            alias=self.KEYSPACE,
            stmt=stmts.select_views_current_days_range,
            params=[offer_id, year, month, day_from, day_to]
        )
        return [_search_coverage_counters_row_mapper.map_from(row._asdict()) for row in rows]
