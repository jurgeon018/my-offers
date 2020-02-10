from cian_core.rabbitmq.consumer import Exchange, Queue, QueueBinding

from my_offers.helpers.queue import get_modified_queue_name


process_announcements_queue = Queue(
    name=get_modified_queue_name('process_announcement'),
    bindings=[
        QueueBinding(
            exchange=Exchange('announcements'),
            routing_key='announcement_reporting.#',
        ),
    ],
)
