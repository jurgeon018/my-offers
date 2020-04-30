# pylint: disable=redefined-outer-name
import pytest
from cian_test_utils import future

from my_offers.services.statistics._cassandra_statistics._views import ViewsCassandraRepository, ViewsRow


@pytest.fixture
def stmts(mocker):
    stmts = mocker.patch(
        'my_offers.services.statistics._cassandra_statistics._views.stmts'
    )
    stmts.select_views_current_days_range = mocker.sentinel.select_views_current_days_range
    stmts.select_views_daily_days_range = mocker.sentinel.select_views_daily_days_range
    return stmts


@pytest.fixture
def cassandra_execute(mocker):
    return mocker.patch(
        'my_offers.services.statistics._cassandra_statistics._views.cassandra_execute',
        autospec=True
    )


class TestDailyOfferShowStatCassandraRepository:

    async def test_get_views_current(self, mocker, stmts, cassandra_execute):
        # arrange

        row = mocker.Mock(spec=['_asdict'])
        row._asdict.return_value = {
            'offer_id': 1,
            'views': 100,
        }

        cassandra_execute.return_value = future([row])

        # act
        result = await ViewsCassandraRepository().get_views_current(
            offer_id=mocker.sentinel.offer_id,
            year=2018,
            month=9,
            day_from=1,
            day_to=10,
        )

        # assert
        assert result == [
            ViewsRow(
                offer_id=1,
                views=100,
            )
        ]
        cassandra_execute.assert_called_once_with(
            alias='statistics',
            params=[mocker.sentinel.offer_id, 2018, 9, 1, 10],
            stmt=mocker.sentinel.select_views_current_days_range
        )

    async def test_get_views_daily(self, mocker, stmts, cassandra_execute):
        # arrange
        row = mocker.Mock(spec=['_asdict'])
        row._asdict.return_value = {
            'offer_id': 1,
            'views': 100,
        }

        cassandra_execute.return_value = future([row])

        # act
        result = await ViewsCassandraRepository().get_views_daily(
            offer_id=mocker.sentinel.offer_id,
            year=2018,
            month=9,
            day_from=1,
            day_to=10,
        )

        # assert
        assert result == [
            ViewsRow(
                offer_id=1,
                views=100,
            )
        ]
        cassandra_execute.assert_called_once_with(
            alias='statistics',
            params=[mocker.sentinel.offer_id, 2018, 9, 1, 10],
            stmt=mocker.sentinel.select_views_daily_days_range
        )
