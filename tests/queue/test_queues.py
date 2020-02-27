from aioamqp_consumer_best import QueueBinding
from cian_core.rabbitmq.consumer import Exchange

from my_offers import enums
from my_offers.queue.queues import _get_bindings


def test__get_bindings(mocker):
    # arrange
    expected = [
        QueueBinding(
            exchange=Exchange('announcements'),
            routing_key='zzz.rent',
        ),
        QueueBinding(
            exchange=Exchange('announcements'),
            routing_key='zzz.sale',
        )
    ]
    
    # act
    result = _get_bindings('zzz', enums.DealType)

    # assert
    assert result[0].routing_key == expected[0].routing_key
    assert result[1].routing_key == expected[1].routing_key
