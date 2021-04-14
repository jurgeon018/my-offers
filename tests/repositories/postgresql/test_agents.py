from datetime import datetime

import pytest
import pytz
from cian_test_utils import future, v
from simple_settings.utils import settings_stub

from my_offers import pg
from my_offers.entities.agents import Agent, AgentName
from my_offers.enums import AgentAccountType
from my_offers.repositories import postgresql
from my_offers.repositories.postgresql.agents import get_agent_names, get_master_user_id


pytestmark = pytest.mark.gen_test


async def test_get_agent__asyncpgsa__query_and_params_compiled_ok():
    # arrange
    pg.get().fetchrow.return_value = future()
    user_id = 1
    query = (
        'SELECT'
        ' agents_hierarchy.id,'
        ' agents_hierarchy.account_type,'
        ' agents_hierarchy.realty_user_id,'
        ' agents_hierarchy.master_agent_user_id,'
        ' agents_hierarchy.row_version,'
        ' agents_hierarchy.created_at,'
        ' agents_hierarchy.updated_at,'
        ' agents_hierarchy.first_name,'
        ' agents_hierarchy.middle_name,'
        ' agents_hierarchy.last_name \n'
        'FROM agents_hierarchy \n'
        'WHERE agents_hierarchy.realty_user_id = $1'
    )
    params = [user_id]

    # act
    await postgresql.get_agent_by_user_id(user_id)

    # assert
    pg.get().fetchrow.assert_called_once_with(query, *params)


async def test_get_agent__record_not_found__return_none():
    # arrange
    pg.get().fetchrow.return_value = future()
    user_id = 1

    # act
    agent = await postgresql.get_agent_by_user_id(user_id)

    # assert
    assert agent is None


async def test_get_agent__record_found__map_from_row():
    # arrange
    agent = v(Agent(
        id=1,
        row_version=0,
        realty_user_id=222,
        master_agent_user_id=333,
        created_at=datetime(2020, 11, 10),
        updated_at=datetime(2020, 11, 12),
        account_type=AgentAccountType.agency,
        first_name='First',
        middle_name='Middle',
        last_name='Last',
    ))

    pg.get().fetchrow.return_value = future({
        'id': agent.id,
        'account_type': agent.account_type,
        'realty_user_id': agent.realty_user_id,
        'master_agent_user_id': agent.master_agent_user_id,
        'row_version': agent.row_version,
        'created_at': agent.created_at,
        'updated_at': agent.updated_at,
        'first_name': agent.first_name,
        'middle_name': agent.middle_name,
        'last_name': agent.last_name,
    })

    # act
    result = await postgresql.get_agent_by_user_id(agent.realty_user_id)

    # assert
    assert result == agent


async def test_save_agent():
    # arrange
    now = datetime.now(pytz.utc)
    agent = v(Agent(
        id=1,
        row_version=0,
        realty_user_id=222,
        master_agent_user_id=333,
        created_at=now,
        updated_at=now,
        account_type=AgentAccountType.agency
    ))
    pg.get().fetchval.return_value = future(1)

    # act
    await postgresql.save_agent(agent=agent)

    # assert
    pg.get().fetchval.assert_called_with(
        'INSERT INTO agents_hierarchy (id, account_type, realty_user_id, master_agent_user_id, row_version,'
        ' created_at, updated_at) VALUES ($3, $1, $5, $4, $7, $2, $8) ON CONFLICT (id) DO UPDATE SET realty'
        '_user_id = excluded.realty_user_id, master_agent_user_id = excluded.master_agent_user_id, row_vers'
        'ion = excluded.row_version, updated_at = excluded.updated_at, first_name = excluded.first_name, mi'
        'ddle_name = excluded.middle_name, last_name = excluded.last_name WHERE agents_hierarchy.row_version < $6',
        agent.account_type.value,
        agent.created_at,
        agent.id,
        agent.master_agent_user_id,
        agent.realty_user_id,
        agent.row_version,
        agent.row_version,
        agent.updated_at,
    )


@pytest.mark.gen_test
async def test_get_master_user_id():
    # arrange
    pg.get().fetchrow.return_value = future({'master_agent_user_id': 12})

    # act
    result = await get_master_user_id(11)

    # assert
    assert result == 12
    pg.get().fetchrow.assert_called_once_with(
        'SELECT master_agent_user_id FROM agents_hierarchy WHERE realty_user_id = $1',
        11
    )


@pytest.mark.gen_test
async def test_get_agent_names():
    # arrange
    pg.get().fetch.return_value = future([{'id': 12, 'first_name': 'Zz', 'last_name': 'Yy', 'middle_name': 'Mm'}])
    expected = [AgentName(id=12, first_name='Zz', last_name='Yy', middle_name='Mm')]

    # act
    with settings_stub(DB_TIMEOUT=3):
        result = await get_agent_names([11])

    # assert
    assert result == expected
    pg.get().fetch.assert_called_once_with(
        '\n        SELECT\n            realty_user_id as id,\n            first_name,\n            middle_name,'
        '\n            last_name\n        FROM\n            agents_hierarchy\n        WHERE'
        '\n            realty_user_id = ANY($1::bigint[])\n    ',
        [11],
        timeout=3,
    )
