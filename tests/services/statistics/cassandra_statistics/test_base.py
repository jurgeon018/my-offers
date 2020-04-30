# pylint: disable=redefined-outer-name
from collections import namedtuple
from datetime import datetime

import pytest
from cian_test_utils import future

from my_offers.services.statistics._cassandra_statistics import BaseStatCassandraRepository
from my_offers.services.statistics._cassandra_statistics._base import StatisticCompletedDateNotAvailable


@pytest.fixture
def stmts(mocker):
    stmts = mocker.patch(
        'my_offers.services.statistics._cassandra_statistics._base.stmts'
    )
    stmts.select_completed_total_date = mocker.sentinel.select_completed_total_date
    return stmts


@pytest.fixture
def cassandra_execute(mocker):
    return mocker.patch(
        'my_offers.services.statistics._cassandra_statistics._base.cassandra_execute',
        autospec=True
    )


class TestBaseOfferShowStatCassandraRepository:
    # pylint: disable=redefined-outer-name

    @pytest.mark.gen_test
    async def test__get_completed_date__call__expected_value(self, stmts, cassandra_execute, mocker):
        # arrange
        Row = namedtuple('Row', ['year', 'month', 'day'])
        cassandra_execute.return_value = future([Row(2017, 10, 2)])

        # act
        result = await BaseStatCassandraRepository()._get_completed_date()

        # assert
        cassandra_execute.assert_called_once_with(
            alias='statistics',
            params=[-1],
            stmt=mocker.sentinel.select_completed_total_date
        )
        assert result == datetime(2017, 10, 2)

    @pytest.mark.gen_test
    async def test__get_completed_date__failed__expected_exception(self, stmts, cassandra_execute):
        # arrange
        cassandra_execute.return_value = future(None)

        # act & assert
        with pytest.raises(StatisticCompletedDateNotAvailable):
            await BaseStatCassandraRepository()._get_completed_date()

    @pytest.mark.gen_test
    async def test_get_completed_date__call__expected_value(self, mocker):
        # arrange
        repo = BaseStatCassandraRepository()
        mocker.patch.object(
            repo,
            '_get_completed_date',
            return_value=future(mocker.sentinel.date)
        )

        # act
        result = await repo.get_completed_date()

        # assert
        assert result == mocker.sentinel.date
        repo._get_completed_date.assert_called_once_with()

    @pytest.mark.gen_test
    async def test_get_completed_date__value_from_cache__expected_value(self, mocker):
        # arrange
        repo = BaseStatCassandraRepository()
        repo.COMPLETED_DATE_CACHE_TTL = 2
        mocker.patch.object(
            repo,
            '_get_completed_date',
            side_effect=[
                future(mocker.sentinel.date1),
                future(mocker.sentinel.date2),
            ]
        )
        time = mocker.patch('my_offers.services.statistics._cassandra_statistics._base.time')
        time.time.side_effect = (1, 2, 4)

        # act
        result1 = await repo.get_completed_date()
        result2 = await repo.get_completed_date()
        result3 = await repo.get_completed_date()

        # assert
        assert result1 == result2 == mocker.sentinel.date1
        assert result3 == mocker.sentinel.date2
        assert repo._get_completed_date.call_count == 2
