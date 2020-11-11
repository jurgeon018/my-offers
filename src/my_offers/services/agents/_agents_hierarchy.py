import logging
from datetime import datetime

import pytz
from asyncpg import UniqueViolationError

from my_offers import pg
from my_offers.entities import AgentMessage
from my_offers.entities.agents import Agent
from my_offers.repositories import postgresql


logger = logging.getLogger(__name__)


async def update_agents_hierarchy(agent: AgentMessage) -> None:
    """ Сохранить/изменить данные об агенте.

        Если master_agent_user_id == None:
            1. Это может быть сам мастер-агент
            2. Это может быть агент без мастера
            3. Это может быть агент у которого больше нет мастера (МА забанили, например)

        account_type может отсутвовать для неидентифицированных агентов или для очень старых аккаунтов.
    """

    if not agent.realty_user_id:
        logger.warning('Agent %s without realty_user_id', agent.id)
        return

    now = datetime.now(pytz.utc)
    agent = Agent(
        id=agent.id,
        row_version=agent.row_version,
        realty_user_id=agent.realty_user_id,
        master_agent_user_id=agent.master_agent_user_id,
        account_type=agent.account_type,
        created_at=now,
        updated_at=now,
        first_name=agent.first_name,
        middle_name=agent.middle_name,
        last_name=agent.last_name,
    )

    try:
        await postgresql.save_agent(agent=agent)
    except UniqueViolationError:
        logger.exception('cannot save agent: %s', agent)
        await _handle_unique_violation_conflict(agent)


async def _handle_unique_violation_conflict(new_agent: Agent) -> None:
    """
    Иногда в очередь приходят сообщения по одному и тому же пользователю,
    но с разными id агента.

    Например, в очередь приходит сообщение
    {
        "id":33791768,
        "realtyUserId":61778933,
        "rowVersion":33873657970,
        ...
    },

    а в базе есть запись
    {
        "id": 33791769,
        "realty_user_id": 61778933,
        "row_version": 33885507106,
        ...
    }.

    У таких агентов айдишник различается на единицу. Предположительно,
    такое сообщение отправляется при откате второй фазы транзакции в C#.

    Задача на исправление в шарпе https://jira.cian.tech/browse/CD-94360
    После фикса этот код выпилить
    """
    old_agent = await postgresql.get_agent_by_user_id(user_id=new_agent.realty_user_id)
    if old_agent is None:
        logger.warning('agent id %s not found', new_agent.id)
        return

    if new_agent.row_version <= old_agent.row_version:
        logger.warning('discard agent changes: old state %s, new state %s', old_agent, new_agent)
        return

    async with pg.get().transaction():
        await postgresql.delete_agents_hierarchy(user_id=old_agent.realty_user_id)
        await postgresql.save_agent(new_agent)
