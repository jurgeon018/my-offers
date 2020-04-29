# pylint: disable=redefined-outer-name
from collections import namedtuple
from datetime import date

import pytest
from cassandra.query import PreparedStatement  # pylint: disable=no-name-in-module
from cian_test_utils import future

from my_offers.services.statistics._cassandra_statistics._coverage import (
    CoverageCassandraRepository,
    StatisticsCoverageRow,
)


@pytest.fixture
def stmts(mocker):
    stmts = mocker.patch(
        'my_offers.services.statistics._cassandra_statistics._coverage.stmts'
    )
    stmts.select_coverage_current = mocker.sentinel.select_coverage_current
    stmts.select_coverage_daily = mocker.sentinel.select_coverage_daily
    stmts.select_coverage_total = mocker.sentinel.select_coverage_total
    return stmts


@pytest.fixture
def cassandra_execute(mocker):
    return mocker.patch(
        'my_offers.services.statistics._cassandra_statistics._coverage.cassandra_execute',
        autospec=True
    )


class TestCoverageCassandraRepository:

    async def test__get_offers_coverage(self, mocker, cassandra_execute):
        # arrange
        Row = namedtuple('Row', ['offer_id', 'favorite_added', 'searches_count'])
        cassandra_execute.return_value = future([
            Row(
                offer_id=1,
                favorite_added=10,
                searches_count=4,
            )
        ])
        statement = mocker.Mock(spec=PreparedStatement)

        # act
        result = await CoverageCassandraRepository()._get_offers_coverage(
            offers_ids=[1],
            date_from=date(2018, 1, 1),
            date_to=date(2019, 1, 2),
            statement=statement,
        )

        # assert
        assert result == [
            StatisticsCoverageRow(
                offer_id=1,
                favorite_added=10,
                searches_count=4,
            ),
        ]
        cassandra_execute.assert_called_once_with(
            alias='statistics',
            stmt=statement,
            params=[[1], date(2018, 1, 1), date(2019, 1, 2)],
        )

    async def test_get_offers_coverage_current(self, mocker, stmts):
        # arrange
        repository = CoverageCassandraRepository()
        mocker.patch.object(repository, '_get_offers_coverage', return_value=future(mocker.sentinel.result))

        # act
        result = await repository.get_offers_coverage_current(
            offers_ids=[1],
            date_from=date(2018, 1, 1),
            date_to=date(2019, 1, 2),
        )

        # assert
        assert result == mocker.sentinel.result
        repository._get_offers_coverage.assert_called_once_with(
            offers_ids=[1],
            date_from=date(2018, 1, 1),
            date_to=date(2019, 1, 2),
            statement=stmts.select_coverage_current,
        )

    async def test_get_offers_coverage_daily(self, mocker, stmts):
        # arrange
        repository = CoverageCassandraRepository()
        mocker.patch.object(repository, '_get_offers_coverage', return_value=future(mocker.sentinel.result))

        # act
        result = await repository.get_offers_coverage_daily(
            offers_ids=[1],
            date_from=date(2018, 1, 1),
            date_to=date(2019, 1, 2),
        )

        # assert
        assert result == mocker.sentinel.result
        repository._get_offers_coverage.assert_called_once_with(
            offers_ids=[1],
            date_from=date(2018, 1, 1),
            date_to=date(2019, 1, 2),
            statement=stmts.select_coverage_daily,
        )

    async def test_get_offers_coverage_total(self, mocker, stmts):
        # arrange
        repository = CoverageCassandraRepository()
        mocker.patch.object(repository, '_get_offers_coverage', return_value=future(mocker.sentinel.result))

        # act
        result = await repository.get_offers_coverage_total(
            offers_ids=[1],
            date_from=date(2018, 1, 1),
            date_to=date(2019, 1, 2),
        )

        # assert
        assert result == mocker.sentinel.result
        repository._get_offers_coverage.assert_called_once_with(
            offers_ids=[1],
            date_from=date(2018, 1, 1),
            date_to=date(2019, 1, 2),
            statement=stmts.select_coverage_total,
        )
