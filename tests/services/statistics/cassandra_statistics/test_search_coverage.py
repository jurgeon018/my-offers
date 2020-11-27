# pylint: disable=redefined-outer-name
from collections import namedtuple
from datetime import date

import pytest
from cian_test_utils import future

from my_offers.services.statistics._cassandra_statistics import SearchCoverageCassandraRepository
from my_offers.services.statistics._cassandra_statistics._search_coverage import SearchCoverageCountersRow


@pytest.fixture
def stmts(mocker):
    stmts = mocker.patch(
        'my_offers.services.statistics._cassandra_statistics._search_coverage.stmts'
    )
    stmts.select_counters = mocker.sentinel.select_counters
    return stmts


@pytest.fixture
def cassandra_execute_grouped(mocker):
    return mocker.patch(
        'my_offers.services.statistics._cassandra_statistics._search_coverage.cassandra_execute_grouped',
        autospec=True
    )


class TestCassandraSearchCoverageRepository:

    async def test__get_offers_coverage(self, mocker, stmts, cassandra_execute_grouped):
        # arrange
        Row = namedtuple('Row', ['offer_id', 'searches_count'])
        cassandra_execute_grouped.return_value = future([
            Row(
                offer_id=1,
                searches_count=2,
            )
        ])

        cassandra_execute_grouped.return_value = future([
            Row(
                offer_id=1,
                searches_count=2,
            )
        ])
        offers_ids = [1]
        # act
        result = await SearchCoverageCassandraRepository().get_offers_counters(
            offers_ids=offers_ids,
            date_from=date(2018, 1, 1),
            date_to=date(2019, 1, 1),
        )

        # assert
        assert result == [
            SearchCoverageCountersRow(
                offer_id=1,
                searches_count=2,
            ),
        ]
        cassandra_execute_grouped.assert_called_once_with(
            alias='search_coverage',
            params=[date(2018, 1, 1), date(2019, 1, 1)],
            stmt=mocker.sentinel.select_counters,
            table='search_coverage.counters',
            keyspace='search_coverage',
            keys=offers_ids
        )
