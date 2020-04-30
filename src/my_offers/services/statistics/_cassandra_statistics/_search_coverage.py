from dataclasses import dataclass
from datetime import date
from typing import List

from cian_cassandra.statement import CassandraStatement
from cian_entities import EntityMapper

from .._helpers import cassandra_execute


stmts = CassandraStatement('search_coverage')
stmts.select_counters = """
SELECT
  offer_id, searches_count
FROM
  search_coverage.counters
WHERE
  offer_id IN ?
  AND date >= ?
  AND date <= ?
"""


@dataclass
class SearchCoverageCountersRow:
    offer_id: int
    searches_count: int


_search_coverage_counters_row_mapper = EntityMapper(
    entity=SearchCoverageCountersRow,
    without_camelcase=True,
)


class SearchCoverageCassandraRepository:
    KEYSPACE = 'search_coverage'

    async def get_offers_counters(
            self,
            offers_ids: List[int],
            date_from: date,
            date_to: date,
    ) -> List[SearchCoverageCountersRow]:
        rows = await cassandra_execute(
            alias=self.KEYSPACE,
            stmt=stmts.select_counters,
            params=[offers_ids, date_from, date_to],
        )
        return [
            _search_coverage_counters_row_mapper.map_from(row._asdict())
            for row in rows
        ]
