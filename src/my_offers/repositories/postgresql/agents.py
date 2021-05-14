from typing import List, Optional

import asyncpgsa
from simple_settings import settings
from sqlalchemy.dialects.postgresql import insert

from my_offers import pg
from my_offers.entities.agents import Agent, AgentHierarchyData, AgentName
from my_offers.mappers.agents import agent_hierarchy_data_mapper, agent_mapper, agent_name_mapper
from my_offers.repositories.postgresql.tables import agents_hierarchy


async def get_agent_by_user_id(user_id: int) -> Optional[Agent]:
    select_query = agents_hierarchy.select().where(agents_hierarchy.c.realty_user_id == user_id)
    query, params = asyncpgsa.compile_query(select_query)
    if row := await pg.get().fetchrow(query, *params):
        return agent_mapper.map_from(row)
    return None


async def save_agent(agent: Agent) -> None:
    insert_values = agent_mapper.map_to(agent)
    insert_query = insert(agents_hierarchy)

    query, params = asyncpgsa.compile_query(
        insert_query.values(
            [insert_values]
        ).on_conflict_do_update(
            index_elements=[agents_hierarchy.c.id],
            where=agents_hierarchy.c.row_version < agent.row_version,
            set_={
                'realty_user_id': insert_query.excluded.realty_user_id,
                'master_agent_user_id': insert_query.excluded.master_agent_user_id,
                'row_version': insert_query.excluded.row_version,
                'updated_at': insert_query.excluded.updated_at,
                'first_name': insert_query.excluded.first_name,
                'middle_name': insert_query.excluded.middle_name,
                'last_name': insert_query.excluded.last_name,
            }
        )
    )

    await pg.get().execute(query, *params)


async def get_master_user_id(user_id: int) -> Optional[int]:
    query = 'SELECT master_agent_user_id FROM agents_hierarchy WHERE realty_user_id = $1'

    row = await pg.get().fetchrow(query, user_id)

    return row['master_agent_user_id'] if row else None


async def get_agent_hierarchy_data(user_id: int) -> AgentHierarchyData:
    query = """
    SELECT * FROM (
        SELECT exists(SELECT id FROM agents_hierarchy WHERE master_agent_user_id = $1) AS is_master_agent,
        (SELECT master_agent_user_id IS NOT NULL FROM agents_hierarchy WHERE realty_user_id = $1) AS is_sub_agent
    ) t
    """
    params = [user_id]
    row = await pg.get().fetchrow(query, *params)
    return agent_hierarchy_data_mapper.map_from(row)


async def get_agent_names(user_ids: List[int]) -> List[AgentName]:
    query = """
        SELECT
            realty_user_id as id,
            first_name,
            middle_name,
            last_name
        FROM
            agents_hierarchy
        WHERE
            realty_user_id = ANY($1::bigint[])
    """

    rows = await pg.get().fetch(query, user_ids, timeout=settings.DB_TIMEOUT)

    return [agent_name_mapper.map_from(row) for row in rows]


async def delete_agents_hierarchy(user_id: int) -> None:
    query = 'delete from agents_hierarchy where realty_user_id = $1 or master_agent_user_id = $1'

    await pg.get().execute(query, user_id)
