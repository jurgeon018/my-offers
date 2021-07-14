from dataclasses import dataclass
from datetime import datetime
from logging import getLogger
from typing import AsyncGenerator

import backoff
import pytz
from cian_core.runtime_settings import runtime_settings
from cian_core.statsd import statsd
from cian_http.exceptions import ApiClientException

from my_offers.helpers.graphite import send_to_graphite
from my_offers.repositories import postgresql
from my_offers.repositories.agents import v1_get_agencies_with_activated_staff_service, v1_get_agents_list
from my_offers.repositories.agents.entities import (
    AgentResponse,
    AgentsListResponse,
    GetAgenciesWithActivatedStaffServiceResponse,
    V1GetAgentsList,
)
from my_offers.repositories.agents.entities.v1_get_agents_list import Statuses
from my_offers.repositories.postgresql.agents import get_sub_agent_ids
from my_offers.services.agents.change_agents_relations import transfer_offers_to_sub_agent


_logger = getLogger(__name__)


@backoff.on_exception(backoff.expo, ApiClientException, max_tries=3)
async def _v1_get_agents_list(request: V1GetAgentsList) -> AgentsListResponse:
    return await v1_get_agents_list(request)


async def sync_agents() -> None:
    response: GetAgenciesWithActivatedStaffServiceResponse = await v1_get_agencies_with_activated_staff_service()
    for master_agent_user_id in response.user_ids:
        try:
            await _sync_master_agent(master_agent_user_id)
        except ApiClientException:
            _logger.exception('cannot sync master agent')


async def _sync_master_agent(master_agent_user_id: int) -> None:
    seen_sub_agents = set()
    async for sub_agent in _paginate_sub_agents(master_agent_user_id):
        await _sync_sub_agent(master_agent_user_id, sub_agent)
        seen_sub_agents.add(sub_agent.user_id)

    all_sub_agents = await get_sub_agent_ids(master_agent_user_id)
    unknown_sub_agents = set(all_sub_agents) - seen_sub_agents
    for sub_agent_realty_user_id in unknown_sub_agents:
        await transfer_offers_to_sub_agent(
            master_agent_user_id,
            sub_agent_realty_user_id,
        )


async def _paginate_sub_agents(master_agent_user_id: int) -> AsyncGenerator[AgentResponse, None]:
    init_paging_data: _InitPagingData = await _init_paging(master_agent_user_id)

    for agent in init_paging_data.agents:
        yield agent

    for page in range(2, init_paging_data.pages_count + 1):
        request = V1GetAgentsList(
            user_id=master_agent_user_id,
            statuses=[Statuses.active],
            page=page,
            page_size=init_paging_data.page_size,
        )
        try:
            response: AgentsListResponse = await _v1_get_agents_list(request)
        except ApiClientException:
            _logger.exception('cannot get agents list')
            continue
        for agent in response.agents:
            yield agent


@dataclass
class _InitPagingData:
    page: int
    page_size: int
    pages_count: int
    agents: list[AgentResponse]


async def _init_paging(master_agent_user_id: int) -> _InitPagingData:
    response: AgentsListResponse = await _v1_get_agents_list(
        V1GetAgentsList(
            user_id=master_agent_user_id,
            statuses=[Statuses.active],
            page=1,
            page_size=runtime_settings.get('GET_AGENTS_LIST_PAGE_SIZE', 10),
        )
    )
    return _InitPagingData(
        page=response.page,
        page_size=response.page_size,
        pages_count=response.pages_count,
        agents=response.agents,
    )


async def _sync_sub_agent(master_agent_user_id: int, sub_agent: AgentResponse) -> None:
    if not sub_agent.state.is_active:
        statsd.incr('sync-agents.skipped')
        return

    is_updated = await postgresql.set_agent_hierarchy_data(
        realty_user_id=sub_agent.user_id,
        master_agent_user_id=master_agent_user_id,
        first_name=sub_agent.first_name,
        last_name=sub_agent.last_name,
        updated_at=datetime.now(pytz.utc),
    )

    if is_updated:
        statsd.incr('sync-agents.updated')
