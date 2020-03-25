from typing import Optional

import asyncpgsa
from sqlalchemy.dialects.postgresql import insert

from my_offers import pg
from my_offers.entities.agents import Agent
from my_offers.mappers.agents import agent_mapper
from my_offers.repositories.postgresql.tables import agents_hierarchy


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
