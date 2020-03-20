import logging
from datetime import datetime

import pytz

from my_offers.entities import AgentMessage
from my_offers.entities.agents import Agent
from my_offers.repositories import postgresql


logger = logging.getLogger(__name__)


async def update_agents_hierarchy(agent: AgentMessage) -> None:
    """ Cохранить/изменить данные об агенте.

        Если master_agent_user_id == None:
            1. Это может быть сам мастер-агент
            2. Это может быть агент без мастера
            3. Это может быть агент у которого больше нет мастера
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
    )
    await postgresql.save_agent(agent=agent)


async def get_master_id_by_subagent(user_id: int) -> int:
    """ Получить ID мастер-аккаунта по ID сабагента. """
    # TODO: https://jira.cian.tech/browse/CD-73807
