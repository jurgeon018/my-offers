from datetime import datetime

import pytest
from cassandra.query import PreparedStatement
from cian_test_utils import future

from my_offers.services.statistics._helpers import cassandra_execute, get_months_intervals, cassandra_execute_grouped


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


async def test_cassandra_execute_grouped(mocker):
    # arrange
    client = mocker.patch('my_offers.services.statistics._helpers.CassandraClient')
    cassandra_execute_mock = mocker.patch('my_offers.services.statistics._helpers.cassandra_execute')
    cassandra_execute_mock.return_value = future([1, 2])
    client.group_keys_by_replica.return_value = [
        [
            (1, ),
            (2, ),
            (3, )
        ], [
            (4, )
        ]
    ]

    stmt = mocker.Mock(spec=PreparedStatement)
    stmt.bind.return_value = mocker.sentinel.stmt
    offer_ids = [1, 2, 3, 4]
    # act
    result = await cassandra_execute_grouped(
        alias='statistics',
        stmt=stmt,
        keys=offer_ids,
        keyspace='statistics',
        table='table',
        params=[5],
        timeout=10
    )

    # assert

    cassandra_execute_mock.assert_has_calls([
        mocker.call(
            params=[[1, 2, 3], 5],
            consistency_level=6,
            stmt=stmt,
            timeout=10,
            alias='statistics'
        ),
        mocker.call(
            params=[[4], 5],
            consistency_level=6,
            stmt=stmt,
            timeout=10,
            alias='statistics'
        ),
    ])

    assert result == [1, 2, 1, 2]
