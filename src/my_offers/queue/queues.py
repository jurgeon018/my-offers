from typing import List, Type

from cian_core.rabbitmq.consumer import Exchange, Queue, QueueBinding
from cian_enum import StrEnum

from my_offers.helpers.queue import get_modified_queue_name
from my_offers.queue.routing_keys import AnnouncementReportingV1RoutingKey


def _get_bindings(prefix: str, enum: Type[StrEnum]) -> List[QueueBinding]:
    result: List[QueueBinding] = []
    values: List[StrEnum] = list(enum)
    for item in values:
        result.append(
            QueueBinding(
                exchange=Exchange('announcements'),
                routing_key='{}.{}'.format(prefix, item.value),
            )
        )

    return result


process_announcements_queue = Queue(
    name=get_modified_queue_name('process_announcement'),
    bindings=_get_bindings('announcement_reporting_v2', AnnouncementReportingV1RoutingKey),
)
