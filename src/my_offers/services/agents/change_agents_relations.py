import asyncio

from my_offers import pg
from my_offers.queue.entities import AgentsRelationsReportingV1ChangedMessage
from my_offers.repositories.agents import v1_get_agent_info_by_id
from my_offers.repositories.agents.entities import V1GetAgentInfoById
from my_offers.repositories.postgresql import update_offer_master_user_id_by_id
from my_offers.repositories.postgresql.agents import set_master_user_id
from my_offers.repositories.postgresql.offer import get_offer_ids_payed_by_user_id


async def change_agents_relations(message: AgentsRelationsReportingV1ChangedMessage) -> None:
    state = message.agent_relation_state

    (
        master_agent_response,
        sub_agent_response,
    ) = await asyncio.gather(
        v1_get_agent_info_by_id(V1GetAgentInfoById(agent_id=message.agent_id)),
        v1_get_agent_info_by_id(V1GetAgentInfoById(agent_id=message.sub_agent_id)),
    )

    master_agent_realty_user_id = master_agent_response.user_id
    sub_agent_realty_user_id = sub_agent_response.user_id

    if state.is_active:
        return await set_master_user_id(
            user_id=sub_agent_realty_user_id,
            new_master_user_id=master_agent_realty_user_id,
        )

    if not any([
        state.is_blocked,
        state.is_deleted,
        state.is_deleted_and_hidden,
    ]):
        return

    payed_by_sub_agent_offer_ids = await get_offer_ids_payed_by_user_id(
        master_user_id=master_agent_realty_user_id,
        user_id=sub_agent_realty_user_id,
    )

    async with pg.get().transaction():
        await set_master_user_id(
            user_id=sub_agent_realty_user_id,
            new_master_user_id=None,
        )
        await asyncio.gather(*[
            update_offer_master_user_id_by_id(
                offer_id=offer_id,
                new_master_user_id=sub_agent_realty_user_id,
            )
            for offer_id in payed_by_sub_agent_offer_ids
        ])
