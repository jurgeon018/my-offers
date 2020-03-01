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

save_announcement_contract_queue = Queue(
    name=get_modified_queue_name('save_announcement_contract'),
    bindings=[
        QueueBinding(
            exchange=Exchange('billing'),
            routing_key='service-contract-reporting.v1.created'
        ),
        QueueBinding(
            exchange=Exchange('billing'),
            routing_key='service-contract-reporting.v1.created'
        )
    ]
)

close_announcement_contract_queue = Queue(
    name=get_modified_queue_name('mark_to_delete_announcement_contract'),
    bindings=[
        QueueBinding(
            exchange=Exchange('billing'),
            routing_key='service-contract-reporting.v1.closed'
        )
    ]
)
