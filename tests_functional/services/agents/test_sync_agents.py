import asyncio
from datetime import datetime, timezone

from cian_functional_test_utils.data_fixtures import load_json_data
from cian_functional_test_utils.pytest_plugin import MockResponse, mock_request
from cian_functional_test_utils.pytest_plugin.telemetry import Increment


async def test_normal_flow__update_expected_sub_agent(runner, agents_mock, pg, mocker):
    # arrange
    await pg.execute(
        """
        INSERT INTO agents_hierarchy (
            id,
            row_version,
            account_type,
            realty_user_id,
            master_agent_user_id,
            created_at,
            updated_at,
            first_name,
            middle_name,
            last_name
        ) VALUES (
            3575024,
            -1,
            null,
            15327749,
            null,
            '2020-04-07 21:18:22.352936',
            '2021-06-24 16:00:13.773588',
            null,
            null,
            null
        ), (
            1,
            -1,
            null,
            2,
            null,
            '2000-01-01 00:00:00.000000',
            '2000-02-01 00:00:00.000000',
            null,
            null,
            null
        )
        """
    )

    await agents_mock.add_stub(
        path='/v1/get-agencies-with-activated-staff-service/',
        method='GET',
        response=MockResponse(
            body={
                'userIds': [
                    48099117,
                ]
            },
        ),
    )

    await agents_mock.add_stub(
        mock_request.query['userId'] == 48099117,
        path='/v1/get-agents-list/',
        method='GET',
        response=MockResponse(
            body=load_json_data(
                __file__,
                'v1_get_agents_list__response__user_48099117.json',
            ),
        ),
    )

    # act
    await runner.run_python_command('sync-agents-command')
    await asyncio.sleep(0.1)
    rows = await pg.fetch('select * from agents_hierarchy order by id')

    # assert
    assert rows == [
        {
            'id': 1,
            'realty_user_id': 2,
            'master_agent_user_id': None,
            'first_name': None,
            'last_name': None,
            'middle_name': None,
            'account_type': None,
            'row_version': -1,
            'created_at': datetime(2000, 1, 1, 0, 0, tzinfo=timezone.utc),
            'updated_at': datetime(2000, 2, 1, 0, 0, tzinfo=timezone.utc),
        },
        {
            'id': 3575024,
            'realty_user_id': 15327749,
            'master_agent_user_id': 48099117,
            'first_name': 'Марина',
            'last_name': 'Морозова',
            'middle_name': None,
            'account_type': None,
            'row_version': -1,
            'created_at': datetime(2020, 4, 7, 21, 18, 22, 352936, tzinfo=timezone.utc),
            'updated_at': mocker.ANY,
        },
    ]


async def test_actual_data__metric_sent(runner, agents_mock, pg, mocker, telemetry):
    # arrange
    await pg.execute(
        """
        INSERT INTO agents_hierarchy (
            id,
            row_version,
            account_type,
            realty_user_id,
            master_agent_user_id,
            created_at,
            updated_at,
            first_name,
            middle_name,
            last_name
        ) VALUES (
            3575024,
            -1,
            null,
            15327749,
            null,
            '2020-04-07 21:18:22.352936',
            '2021-06-24 16:00:13.773588',
            null,
            null,
            null
        )
        """
    )

    await agents_mock.add_stub(
        path='/v1/get-agencies-with-activated-staff-service/',
        method='GET',
        response=MockResponse(
            body={
                'userIds': [
                    48099117,
                ]
            },
        ),
    )

    await agents_mock.add_stub(
        mock_request.query['userId'] == 48099117,
        path='/v1/get-agents-list/',
        method='GET',
        response=MockResponse(
            body=load_json_data(
                __file__,
                'v1_get_agents_list__response__user_48099117.json',
            ),
        ),
    )

    # act
    await runner.run_python_command('sync-agents-command')
    await asyncio.sleep(0.1)
    metrics = telemetry.get_sent()

    # assert
    assert Increment('sync-agents.updated') in metrics
