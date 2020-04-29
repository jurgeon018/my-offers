from datetime import datetime

import pytest
from cassandra.query import PreparedStatement
from cian_test_utils import future

from my_offers.services.statistics._helpers import cassandra_execute, get_months_intervals


@pytest.mark.parametrize(('date_from', 'date_to', 'expected'), [
    (datetime(2017, 7, 25), datetime(2017, 7, 25), [(
        datetime(2017, 7, 25, 0, 0),
        datetime(2017, 7, 25, 0, 0),
    )]),
    (datetime(2017, 7, 25), datetime(2017, 7, 28), [(
        datetime(2017, 7, 25, 0, 0),
        datetime(2017, 7, 28, 0, 0),
    )]),
    (datetime(2017, 7, 25), datetime(2017, 7, 31), [(
        datetime(2017, 7, 25, 0, 0),
        datetime(2017, 7, 31, 0, 0),
    )]),
    (datetime(2017, 7, 1), datetime(2017, 7, 31), [(
        datetime(2017, 7, 1, 0, 0),
        datetime(2017, 7, 31, 0, 0),
    )]),
    (datetime(2017, 7, 1), datetime(2017, 8, 1), [(
        datetime(2017, 7, 1, 0, 0),
        datetime(2017, 7, 31, 0, 0),
    ), (
        datetime(2017, 8, 1, 0, 0),
        datetime(2017, 8, 1, 0, 0),
    )]),
    (datetime(2017, 7, 1), datetime(2017, 8, 31), [(
        datetime(2017, 7, 1, 0, 0),
        datetime(2017, 7, 31, 0, 0),
    ), (
        datetime(2017, 8, 1, 0, 0),
        datetime(2017, 8, 31, 0, 0),
    )]),
    (datetime(2017, 7, 1), datetime(2017, 9, 15), [(
        datetime(2017, 7, 1, 0, 0),
        datetime(2017, 7, 31, 0, 0),
    ), (
        datetime(2017, 8, 1, 0, 0),
        datetime(2017, 8, 31, 0, 0),
    ), (
        datetime(2017, 9, 1, 0, 0),
        datetime(2017, 9, 15, 0, 0),
    )]),
    (datetime(2017, 7, 31), datetime(2017, 8, 7), [(
        datetime(2017, 7, 31, 0, 0),
        datetime(2017, 7, 31, 0, 0),
    ), (
        datetime(2017, 8, 1, 0, 0),
        datetime(2017, 8, 7, 0, 0),
    )]),
    (datetime(2017, 12, 15), datetime(2018, 1, 15), [(
        datetime(2017, 12, 15, 0, 0),
        datetime(2017, 12, 31, 0, 0),
    ), (
        datetime(2018, 1, 1, 0, 0),
        datetime(2018, 1, 15, 0, 0),
    )])
])
def test_get_months_intervals(date_from, date_to, expected):
    assert get_months_intervals(date_from, date_to) == expected


async def test_cassandra_execute(mocker):
    # arrange
    client = mocker.patch('my_offers.services.statistics._helpers.CassandraClient')
    client.execute.return_value = future(mocker.sentinel.result)

    stmt = mocker.Mock(spec=PreparedStatement)
    stmt.bind.return_value = mocker.sentinel.stmt

    # act
    await cassandra_execute(
        alias='statistics',
        stmt=stmt,
        params=mocker.sentinel.params,
        timeout=10
    )

    # assert
    client.execute.assert_called_once_with(
        mocker.sentinel.stmt,
        timeout=10,
        alias='statistics'
    )
    stmt.bind.assert_called_once_with(mocker.sentinel.params)
