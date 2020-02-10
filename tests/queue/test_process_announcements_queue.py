from datetime import datetime

import pytest
from cian_core.rabbitmq.consumer import Message
from cian_test_utils import future

from my_offers.queue.consumers import process_announcement_callback
from my_offers.queue.entities import AnnouncementMessage


@pytest.mark.gen_test
async def test_process_announcements_queue(mocker):
    # arrange
    message = mocker.Mock(spec=Message)
    model = mocker.sentinel.model
    message.data = AnnouncementMessage(
        model=mocker.sentinel.model,
        operation_id='zzzzzzzzzzzzzzz',
        date=datetime(2019, 1, 1),
    )

    process_announcement_mock = mocker.patch(
        'my_offers.queue.consumers.process_announcement',
        return_value=future(),
    )
    new_operation_id_mock = mocker.patch('my_offers.queue.consumers.new_operation_id')
    new_operation_id_mock.return_value.__enter__.return_value = 'zzzzzzzzzzzzzzz'

    # act
    await process_announcement_callback([message])

    # assert
    process_announcement_mock.assert_called_once_with(model)
    new_operation_id_mock.assert_called_once_with('zzzzzzzzzzzzzzz')
