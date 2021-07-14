from datetime import datetime

import pytest
import pytz
from cian_http.exceptions import ApiClientException, TimeoutException
from cian_test_utils import future, v
from freezegun import freeze_time

from my_offers.repositories.agents.entities import (
    AgentResponse,
    AgentsListResponse,
    GetAgenciesWithActivatedStaffServiceResponse,
)
from my_offers.repositories.agents.entities.agent_response import State
from my_offers.services.agents import sync_agents


@pytest.fixture(name='patch_v1_get_agencies_with_activated_staff_service')
def patch_v1_get_agencies_with_activated_staff_service_fixture(mocker):
    def _factory(*, user_ids):
        return mocker.patch.object(
            sync_agents,
            'v1_get_agencies_with_activated_staff_service',
            return_value=future(
                v(
                    GetAgenciesWithActivatedStaffServiceResponse(
                        user_ids=user_ids,
                    ),
                ),
            )
        )

    return _factory


async def test_sync_agents__multiple_master_agents_returned__sync_all_master_agents(
        patch_v1_get_agencies_with_activated_staff_service,
        mocker,
):
    # arrange
    patch_v1_get_agencies_with_activated_staff_service(user_ids=[1, 2])

    _sync_master_agent_mock = mocker.patch.object(
        sync_agents,
        '_sync_master_agent',
        return_value=future(),
    )

    # act
    await sync_agents.sync_agents()

    # assert
    assert _sync_master_agent_mock.call_args_list == [
        mocker.call(1),
        mocker.call(2),
    ]


async def test_sync_master_agent__multiple_sub_agents_returned__sync_all_sub_agents(
        patch_v1_get_agencies_with_activated_staff_service,
        mocker,
):
    # arrange
    master_agent_user_id = 1

    patch_v1_get_agencies_with_activated_staff_service(user_ids=[master_agent_user_id])

    sub_agent_1 = v(
        AgentResponse(
            phones=[],
            state=State.active,
            user_id=2,
        ),
    )

    sub_agent_2 = v(
        AgentResponse(
            phones=[],
            state=State.active,
            user_id=3,
        ),
    )

    mocker.patch.object(
        sync_agents,
        'v1_get_agents_list',
        return_value=future(
            v(
                AgentsListResponse(
                    agents=[
                        sub_agent_1,
                        sub_agent_2,
                    ],
                    page=1,
                    page_size=10,
                    pages_count=1,
                    total_count=2,
                )
            ),
        ),
    )

    _sync_sub_agent = mocker.patch.object(
        sync_agents,
        '_sync_sub_agent',
        return_value=future(),
    )

    mocker.patch.object(
        sync_agents,
        'get_sub_agent_ids',
        return_value=future([]),
    )

    # act
    await sync_agents.sync_agents()

    # assert
    assert _sync_sub_agent.call_args_list == [
        mocker.call(master_agent_user_id, sub_agent_1),
        mocker.call(master_agent_user_id, sub_agent_2),
    ]


async def test_sync_master_agent__timeout_while_fetching_sub_agents__retry_up_to_3_times(
        patch_v1_get_agencies_with_activated_staff_service,
        mocker,
):
    # arrange
    master_agent_user_id = 1

    patch_v1_get_agencies_with_activated_staff_service(user_ids=[master_agent_user_id])

    sub_agent_1 = v(
        AgentResponse(
            phones=[],
            state=State.active,
            user_id=2,
        ),
    )

    mocker.patch.object(
        sync_agents,
        'v1_get_agents_list',
        side_effect=[
            future(exception=TimeoutException(message='')),
            future(exception=TimeoutException(message='')),
            future(
                v(
                    AgentsListResponse(
                        agents=[
                            sub_agent_1,
                        ],
                        page=1,
                        page_size=10,
                        pages_count=1,
                        total_count=1,
                    )
                ),
            ),
            RuntimeError,  # терминирует ситуацию, когда мок вызывается большее количество раз, чем ожидалось
        ],
    )

    _sync_sub_agent = mocker.patch.object(
        sync_agents,
        '_sync_sub_agent',
        return_value=future(),
    )

    mocker.patch.object(
        sync_agents,
        'get_sub_agent_ids',
        return_value=future([]),
    )

    # act
    await sync_agents.sync_agents()

    # assert
    assert _sync_sub_agent.call_args_list == [
        mocker.call(master_agent_user_id, sub_agent_1),
    ]


async def test_sync_master_agent__api_client_exception_while_fetching_sub_agents__skip_sub_agent(
        patch_v1_get_agencies_with_activated_staff_service,
        mocker,
):
    # arrange
    patch_v1_get_agencies_with_activated_staff_service(user_ids=[1])

    sub_agent_1 = v(
        AgentResponse(
            phones=[],
            state=State.active,
            user_id=2,
        ),
    )

    mocker.patch.object(
        sync_agents,
        'v1_get_agents_list',
        side_effect=[
            future(
                v(
                    AgentsListResponse(
                        agents=[
                            sub_agent_1,
                        ],
                        page=1,
                        page_size=1,
                        pages_count=2,
                        total_count=2,
                    )
                ),
            ),
            future(exception=ApiClientException(message='')),
            future(exception=ApiClientException(message='')),
            future(exception=ApiClientException(message='')),
            RuntimeError,  # терминирует ситуацию, когда мок вызывается большее количество раз, чем ожидалось
        ],
    )

    _logger = mocker.patch.object(sync_agents, '_logger')

    mocker.patch.object(
        sync_agents,
        '_sync_sub_agent',
        return_value=future(),
    )

    mocker.patch.object(
        sync_agents,
        'get_sub_agent_ids',
        return_value=future([]),
    )

    # act
    await sync_agents.sync_agents()

    # assert
    _logger.exception.assert_called_once_with('cannot get agents list')


async def test_sync_master_agent__multiple_pages_exist__process_all_pages(
        patch_v1_get_agencies_with_activated_staff_service,
        mocker,
):
    # arrange
    master_agent_user_id = 1

    patch_v1_get_agencies_with_activated_staff_service(user_ids=[master_agent_user_id])

    sub_agent_1 = v(
        AgentResponse(
            phones=[],
            state=State.active,
            user_id=2,
        ),
    )

    sub_agent_2 = v(
        AgentResponse(
            phones=[],
            state=State.active,
            user_id=3,
        ),
    )

    mocker.patch.object(
        sync_agents,
        'v1_get_agents_list',
        side_effect=[
            future(
                v(
                    AgentsListResponse(
                        agents=[
                            sub_agent_1,
                        ],
                        page=1,
                        page_size=1,
                        pages_count=2,
                        total_count=2,
                    )
                ),
            ),
            future(
                v(
                    AgentsListResponse(
                        agents=[
                            sub_agent_2,
                        ],
                        page=2,
                        page_size=1,
                        pages_count=2,
                        total_count=2,
                    )
                ),
            ),
            RuntimeError,  # терминирует ситуацию, когда мок вызывается большее количество раз, чем ожидалось
        ],
    )

    _sync_sub_agent = mocker.patch.object(
        sync_agents,
        '_sync_sub_agent',
        return_value=future(),
    )

    mocker.patch.object(
        sync_agents,
        'get_sub_agent_ids',
        return_value=future([]),
    )

    # act
    await sync_agents.sync_agents()

    # assert
    assert _sync_sub_agent.call_args_list == [
        mocker.call(master_agent_user_id, sub_agent_1),
        mocker.call(master_agent_user_id, sub_agent_2),
    ]


async def test_sync_sub_agent__active_state__update_agent_info(
        patch_v1_get_agencies_with_activated_staff_service,
        mocker,
):
    # arrange
    master_agent_user_id = 1

    patch_v1_get_agencies_with_activated_staff_service(user_ids=[master_agent_user_id])

    sub_agent = v(
        AgentResponse(
            phones=[],
            state=State.active,
            user_id=2,
            first_name='Марина',
            last_name='Морозова',
        ),
    )

    mocker.patch.object(
        sync_agents,
        'v1_get_agents_list',
        return_value=future(
            v(
                AgentsListResponse(
                    agents=[
                        sub_agent,
                    ],
                    page=1,
                    page_size=10,
                    pages_count=1,
                    total_count=1,
                )
            ),
        ),
    )

    set_agent_hierarchy_data = mocker.patch.object(
        sync_agents.postgresql,
        'set_agent_hierarchy_data',
        return_value=future(1),
    )

    mocker.patch.object(
        sync_agents,
        'get_sub_agent_ids',
        return_value=future([]),
    )

    incr = mocker.patch.object(sync_agents.statsd, 'incr')

    now = datetime(2000, 1, 2, tzinfo=pytz.utc)

    # act
    with freeze_time(now):
        await sync_agents.sync_agents()

    # assert
    incr.assert_called_once_with('sync-agents.updated')
    set_agent_hierarchy_data.assert_called_once_with(
        realty_user_id=sub_agent.user_id,
        master_agent_user_id=master_agent_user_id,
        first_name=sub_agent.first_name,
        last_name=sub_agent.last_name,
        updated_at=now,
    )


async def test_sync_sub_agent__extra_sub_agents_found__transfer_offers(
        patch_v1_get_agencies_with_activated_staff_service,
        mocker,
):
    # arrange
    master_agent_user_id = 1

    patch_v1_get_agencies_with_activated_staff_service(user_ids=[master_agent_user_id])

    sub_agent = v(
        AgentResponse(
            phones=[],
            state=State.active,
            user_id=2,
            first_name='Марина',
            last_name='Морозова',
        ),
    )

    mocker.patch.object(
        sync_agents,
        'v1_get_agents_list',
        return_value=future(
            v(
                AgentsListResponse(
                    agents=[
                        sub_agent,
                    ],
                    page=1,
                    page_size=10,
                    pages_count=1,
                    total_count=1,
                )
            ),
        ),
    )

    mocker.patch.object(
        sync_agents.postgresql,
        'set_agent_hierarchy_data',
        return_value=future(1),
    )

    mocker.patch(
        'my_offers.services.agents.change_agents_relations.get_offer_ids_payed_by_user_id',
        return_value=future([5, 6]),
    )

    mocker.patch(
        'my_offers.services.agents.change_agents_relations.set_master_user_id',
        return_value=future(),
    )

    update_offer_master_user_id_by_id = mocker.patch(
        'my_offers.services.agents.change_agents_relations.update_offer_master_user_id_by_id',
        side_effect=[future(), future(), Exception],
    )

    mocker.patch.object(
        sync_agents,
        'get_sub_agent_ids',
        return_value=future([2, 3]),
    )

    now = datetime(2000, 1, 2, tzinfo=pytz.utc)

    # act
    with freeze_time(now):
        await sync_agents.sync_agents()

    # assert
    assert update_offer_master_user_id_by_id.call_args_list == [
        mocker.call(new_master_user_id=3, offer_id=5),
        mocker.call(new_master_user_id=3, offer_id=6),
    ]


@pytest.mark.parametrize('state', [
    state for state in State
    if state != State.active
])
async def test_sync_sub_agent__not_active_state__metric_sent(
        patch_v1_get_agencies_with_activated_staff_service,
        mocker,
        state,
):
    # arrange
    master_agent_user_id = 1

    patch_v1_get_agencies_with_activated_staff_service(user_ids=[master_agent_user_id])

    sub_agent = v(
        AgentResponse(
            phones=[],
            state=state,
            user_id=2,
            first_name='Марина',
            last_name='Морозова',
        ),
    )

    mocker.patch.object(
        sync_agents,
        'v1_get_agents_list',
        return_value=future(
            v(
                AgentsListResponse(
                    agents=[
                        sub_agent,
                    ],
                    page=1,
                    page_size=10,
                    pages_count=1,
                    total_count=1,
                )
            ),
        ),
    )

    set_agent_hierarchy_data = mocker.patch.object(
        sync_agents.postgresql,
        'set_agent_hierarchy_data',
        return_value=future(None),
    )

    mocker.patch.object(
        sync_agents,
        'get_sub_agent_ids',
        return_value=future([]),
    )

    incr = mocker.patch.object(sync_agents.statsd, 'incr')

    now = datetime(2000, 1, 2, tzinfo=pytz.utc)

    # act
    with freeze_time(now):
        await sync_agents.sync_agents()

    # assert
    incr.assert_called_once_with('sync-agents.skipped')
    set_agent_hierarchy_data.assert_not_called()
