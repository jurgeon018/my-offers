from datetime import datetime
from typing import Generator

import backoff
import pytz
from cian_core.runtime_settings import runtime_settings
from cian_core.statsd import statsd
from cian_http.exceptions import TimeoutException

from my_offers.repositories import postgresql
from my_offers.repositories.agents import (
    v1_get_agencies_with_activated_staff_service, v1_get_agents_list)
from my_offers.repositories.agents.entities import (
    AgentResponse, AgentsListResponse,
    GetAgenciesWithActivatedStaffServiceResponse, V1GetAgentsList)


@backoff.on_exception(backoff.expo, TimeoutException, max_tries=3)
async def _v1_get_agents_list(request: V1GetAgentsList) -> AgentsListResponse:
    return await v1_get_agents_list(request)


async def sync_agents() -> None:
    response: GetAgenciesWithActivatedStaffServiceResponse = await v1_get_agencies_with_activated_staff_service()
    for master_agent_user_id in response.user_ids:
        await _sync_master_agent(master_agent_user_id)


async def _sync_master_agent(master_agent_user_id: int) -> None:
    async for sub_agent in _paginate_sub_agents(master_agent_user_id):
        await _sync_sub_agent(master_agent_user_id, sub_agent)


async def _paginate_sub_agents(master_agent_user_id: int) -> Generator[AgentResponse, None, None]:
    page = 1
    page_size = runtime_settings.get('GET_AGENTS_LIST_PAGE_SIZE', 10)
    response: AgentsListResponse = await _v1_get_agents_list(
        V1GetAgentsList(
            user_id=master_agent_user_id,
            page=page,
            page_size=page_size,
        )
    )
    for agent in response.agents:
        yield agent
    for page in range(2, response.pages_count + 1):
        response: AgentsListResponse = await _v1_get_agents_list(
            V1GetAgentsList(
                user_id=master_agent_user_id,
                page=page,
                page_size=page_size,
            )
        )
        for agent in response.agents:
            yield agent


async def _sync_sub_agent(master_agent_user_id: int, sub_agent: AgentResponse) -> None:
    if not sub_agent.state.is_active:
        statsd.incr('sync-agents.skipped')
        return
    if await postgresql.set_agent_hierarchy_data(
        realty_user_id=sub_agent.user_id,
        master_agent_user_id=master_agent_user_id,
        first_name=sub_agent.first_name,
        last_name=sub_agent.last_name,
        updated_at=datetime.now(pytz.utc),
    ):
        statsd.incr('sync-agents.updated')
