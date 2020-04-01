import pytest
from cian_core.rabbitmq.consumer import Message
from cian_test_utils import future, v

from my_offers.entities import AgentMessage
from my_offers.queue.consumers import save_agent_callback


pytestmark = pytest.mark.gen_test


async def test_save_agent_callback(mocker):
    # arrange
    operation_id = '213123231'
    event = v(AgentMessage(
        id=1,
        row_version=0,
        realty_user_id=222,
        master_agent_user_id=333,
        operation_id=operation_id
    ))
    message = mocker.Mock(spec=Message)
    message.data = event
    save_offer_offence_mock = mocker.patch(
        'my_offers.queue.consumers.update_agents_hierarchy',
        return_value=future()
    )
    new_operation_id_mock = mocker.patch('my_offers.queue.consumers.new_operation_id')
    new_operation_id_mock.return_value.__enter__.return_value = operation_id

    # act
    await save_agent_callback([message])

    # assert
    save_offer_offence_mock.assert_called_with(agent=event)
    new_operation_id_mock.assert_called_with(operation_id)