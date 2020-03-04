from collections import namedtuple
from datetime import datetime

import pytest
from cian_core.rabbitmq.consumer import Message
from cian_test_utils import future

from my_offers.queue.consumers import process_announcement_callback
from my_offers.queue.entities import AnnouncementMessage
from my_offers.repositories.monolith_cian_announcementapi.entities import BargainTerms, ObjectModel, Phone
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category


@pytest.mark.gen_test
async def test_process_announcements_queue(mocker):
    # arrange
    Envelope = namedtuple('Envelope', ['routing_key'])
    envelope = Envelope(routing_key=mocker.sentinel.routing_key)
    message = mocker.Mock(spec=Message)
    message.envelope = envelope
    model = ObjectModel(
        id=111,
        bargain_terms=BargainTerms(price=123),
        category=Category.flat_rent,
        phones=[Phone(country_code='1', number='12312')],
        cian_id=333,
        row_version=111,
    )
    message.data = AnnouncementMessage(
        model=model,
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


@pytest.mark.gen_test
async def test_process_announcements_queue__exception__raise(mocker):
    # arrange
    Envelope = namedtuple('Envelope', ['routing_key'])
    envelope = Envelope(routing_key=mocker.sentinel.routing_key)
    message = mocker.Mock(spec=Message)
    message.envelope = envelope
    model = ObjectModel(
        id=111,
        bargain_terms=BargainTerms(price=123),
        category=Category.flat_rent,
        phones=[Phone(country_code='1', number='12312')],
        cian_id=333,
        row_version=111,
    )
    message.data = AnnouncementMessage(
        model=model,
        operation_id='zzzzzzzzzzzzzzz',
        date=datetime(2019, 1, 1),
    )

    process_announcement_mock = mocker.patch(
        'my_offers.queue.consumers.process_announcement',
        return_value=future(exception=TypeError('zzz')),
    )
    new_operation_id_mock = mocker.patch('my_offers.queue.consumers.new_operation_id')
    new_operation_id_mock.return_value.__enter__.return_value = 'zzzzzzzzzzzzzzz'

    # act
    with pytest.raises(TypeError):
        await process_announcement_callback([message])

    # assert
    process_announcement_mock.assert_called_once_with(model)
    new_operation_id_mock.assert_called_once_with('zzzzzzzzzzzzzzz')
