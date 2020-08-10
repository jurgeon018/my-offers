from dataclasses import dataclass
from datetime import date
from typing import List

from cassandra.query import PreparedStatement  # pylint: disable=no-name-in-module
from cian_cassandra.statement import CassandraStatement
from cian_entities import EntityMapper

from .._helpers import cassandra_execute


_query_template = """
SELECT
  offer_id, favorite_added, search_results_shown as searches_count
FROM
  statistics.coverage_{type}
WHERE
  offer_id IN ?
  AND date >= ?
  AND date <= ?
"""
stmts = CassandraStatement('statistics')
stmts.select_coverage_current = _query_template.format(type='current')
stmts.select_coverage_daily = _query_template.format(type='daily_v2')
stmts.select_coverage_total = _query_template.format(type='total_v2')


@dataclass
class StatisticsCoverageRow:
    offer_id: int
    favorite_added: int
    searches_count: int


_search_coverage_mapper = EntityMapper(
    entity=StatisticsCoverageRow,
    without_camelcase=True,
)


class CoverageCassandraRepository:
    KEYSPACE = 'statistics'

    async def get_offers_coverage_current(
            self,
            offers_ids: List[int],
            date_from: date,
            date_to: date,
    ) -> List[StatisticsCoverageRow]:
        return (await self._get_offers_coverage(
            offers_ids=offers_ids,
            date_from=date_from,
            date_to=date_to,
            statement=stmts.select_coverage_current,
        ))

    async def get_offers_coverage_total(
            self,
            offers_ids: List[int],
            date_from: date,
            date_to: date,
    ) -> List[StatisticsCoverageRow]:
        return (await self._get_offers_coverage(
            offers_ids=offers_ids,
            date_from=date_from,
            date_to=date_to,
            statement=stmts.select_coverage_total,
        ))

    async def get_offers_coverage_daily(
            self,
            offers_ids: List[int],
            date_from: date,
            date_to: date,
    ) -> List[StatisticsCoverageRow]:
        return (await self._get_offers_coverage(
            offers_ids=offers_ids,
            date_from=date_from,
            date_to=date_to,
            statement=stmts.select_coverage_daily,
        ))

    async def _get_offers_coverage(
            self,
            offers_ids: List[int],
            date_from: date,
            date_to: date,
            statement: PreparedStatement,
    ) -> List[StatisticsCoverageRow]:
        rows = await cassandra_execute(
            alias=self.KEYSPACE,
            stmt=statement,
            params=[offers_ids, date_from, date_to],
        )
        return [
            _search_coverage_mapper.map_from(row._asdict())
            for row in rows
        ]
