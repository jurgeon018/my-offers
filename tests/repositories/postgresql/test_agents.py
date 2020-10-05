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

    # act
    await postgresql.save_agent(agent=agent)

    # assert
    pg.get().execute.assert_called_with(
        'INSERT INTO agents_hierarchy (id, account_type, realty_user_id, master_agent_user_id, row_version, '
        'created_at, updated_at) VALUES ($3, $1, $5, $4, $7, $2, $8) ON CONFLICT (id) DO UPDATE '
        'SET realty_user_id = excluded.realty_user_id, master_agent_user_id = excluded.master_agent_user_id, '
        'row_version = excluded.row_version, updated_at = excluded.updated_at, first_name = excluded.first_name, '
        'middle_name = excluded.middle_name, last_name = excluded.last_name WHERE agents_hierarchy.row_version < $6',
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
