import asyncio
from pathlib import Path

import pytest
from cian_functional_test_utils.data_fixtures import load_json_data
from cian_functional_test_utils.pytest_plugin import MockResponse, mock_request


@pytest.fixture(autouse=True)
async def _start(runner, queue_service):
    await runner.start_background_python_command('agents_relations_changed_consumer')
    await queue_service.wait_consumer('my-offers.agents_relations_changed')


@pytest.mark.parametrize('state', ['Request', 'Active', 'Processing'])
async def test_not_interesting_states__do_nothing(queue_service, state, pg):
    # arrange
    await pg.execute_scripts(Path(__file__).parent / 'data' / 'setup.sql')

    # act
    await queue_service.publish(
        'agents-relations-reporting.v1.changed',
        load_json_data(__file__, f'agents-relations-reporting.v1.changed--{state}.json'),
        exchange='sub-agents',
    )
    await asyncio.sleep(0.5)
    row = await pg.fetchrow('select master_user_id, user_id from offers where offer_id = $1', [173975523])

    # assert
    assert row == {'master_user_id': 3, 'user_id': 4}


@pytest.mark.parametrize('state', ['Blocked', 'Deleted', 'DeletedAndHidden'])
async def test_interesting_states__update_hierarchy(queue_service, state, pg, agents_mock):
    # arrange
    await pg.execute_scripts(Path(__file__).parent / 'data' / 'setup.sql')

    await asyncio.gather(
        agents_mock.add_stub(
            mock_request.query['agentId'] == 1,
            method='GET',
            path='/v1/get-agent-info-by-id/',
            response=MockResponse(
                body={
                    'userId': 3,
                    'agentId': 1,
                    'agentType': 'agent',
                },
            ),
        ),
        agents_mock.add_stub(
            mock_request.query['agentId'] == 2,
            method='GET',
            path='/v1/get-agent-info-by-id/',
            response=MockResponse(
                body={
                    'userId': 4,
                    'agentId': 2,
                    'agentType': 'agent',
                },
            ),
        ),
    )

    # act
    await queue_service.publish(
        'agents-relations-reporting.v1.changed',
        load_json_data(__file__, f'agents-relations-reporting.v1.changed--{state}.json'),
        exchange='sub-agents',
    )
    await asyncio.sleep(0.5)
    master_agent_offer_row = await pg.fetchrow('select master_user_id, user_id from offers where offer_id = $1', [173975523])
    sub_agent_offer_row = await pg.fetchrow('select master_user_id, user_id from offers where offer_id = $1', [173975524])

    # assert
    assert master_agent_offer_row == {'master_user_id': 3, 'user_id': 4}
    assert sub_agent_offer_row == {'master_user_id': 4, 'user_id': 4}
