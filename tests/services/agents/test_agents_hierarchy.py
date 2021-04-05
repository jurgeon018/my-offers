from datetime import datetime

import pytz
from asyncpg import UniqueViolationError
from cian_test_utils import future, v
from freezegun import freeze_time

from my_offers.entities import AgentMessage
from my_offers.entities.agents import Agent
from my_offers.enums import AgentAccountType
from my_offers.services import agents


async def test_update_agents_hierarchy(mocker):
    # arrange
    now = datetime.now(pytz.utc)
    expected_agent = v(Agent(
        id=1,
        row_version=0,
        realty_user_id=222,
        master_agent_user_id=333,
        created_at=now,
        updated_at=now,
        account_type=AgentAccountType.agency
    ))
    agent = v(AgentMessage(
        id=1,
        row_version=0,
        realty_user_id=222,
        master_agent_user_id=333,
        account_type=AgentAccountType.agency
    ))
    mocker.patch(
        'my_offers.services.agents._agents_hierarchy.postgresql.get_agent_by_user_id',
        return_value=future()
    )

    save_agent_mock = mocker.patch(
        'my_offers.services.agents._agents_hierarchy.postgresql.save_agent',
        return_value=future()
    )

    # act
    with freeze_time(now):
        await agents.update_agents_hierarchy(agent=agent)

    # assert
    save_agent_mock.assert_called_with(agent=expected_agent)


async def test_update_agents_hierarchy__realty_user_id_is_none(mocker):
    # arrange
    agent = v(AgentMessage(
        id=1,
        row_version=0,
        realty_user_id=None,
        master_agent_user_id=333,
    ))
    save_agent_mock = mocker.patch(
        'my_offers.services.agents._agents_hierarchy.postgresql.save_agent',
        return_value=future()
    )
    logger = mocker.patch('my_offers.services.agents._agents_hierarchy.logger')

    # act
    await agents.update_agents_hierarchy(agent=agent)

    # assert
    logger.warning.assert_called_with('Agent %s without realty_user_id', agent.id)
    save_agent_mock.assert_not_called()


async def test_update_agents_hierarchy__unique_violation_error__agent_not_found(mocker):
    # arrange
    agent = v(AgentMessage(
        id=1,
        row_version=0,
        realty_user_id=222,
        master_agent_user_id=333,
        account_type=AgentAccountType.agency
    ))
    mocker.patch(
        'my_offers.services.agents._agents_hierarchy.postgresql.save_agent',
        return_value=future(exception=UniqueViolationError())
    )
    mocker.patch(
        'my_offers.services.agents._agents_hierarchy.postgresql.get_agent_by_user_id',
        return_value=future()
    )
    logger = mocker.patch('my_offers.services.agents._agents_hierarchy.logger')

    # act
    await agents.update_agents_hierarchy(agent=agent)

    # assert
    logger.warning.assert_called_with('agent id %s not found', agent.id)
