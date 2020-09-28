from typing import List, Type

from cian_core.rabbitmq.consumer import Exchange, Queue, QueueBinding
from cian_enum import StrEnum

from my_offers.helpers.queue import get_modified_queue_name
from my_offers.queue.routing_keys import (
    AgentsReportingV1RoutingKey,
    AnnouncementPremoderationReportingV1RoutingKey,
    AnnouncementReportingV1RoutingKey,
    ModerationOfferOffenceReportingV1RoutingKey,
    OfferDuplicateV1RoutingKey,
    OffersResendV1RoutingKey,
    ServiceContractsReportingV1RoutingKey,
    UnloadOrderReportingV1RoutingKey,
)


my_offers_exchange = Exchange('my-offers')
billing_exchange = Exchange('billing')


def _get_bindings(exchange: str, prefix: str, enum: Type[StrEnum]) -> List[QueueBinding]:
    result: List[QueueBinding] = []
    values: List[StrEnum] = list(enum)
    for item in values:
        result.append(
            QueueBinding(
                exchange=Exchange(exchange),
                routing_key='{}.{}'.format(prefix, item.value),
            )
        )

    return result


process_announcements_queue = Queue(
    name=get_modified_queue_name('process_announcement_v2'),
    bindings=_get_bindings('announcements', 'announcement_reporting', AnnouncementReportingV1RoutingKey),
)

process_announcements_from_elasticapi = Queue(
    name=get_modified_queue_name('process_announcement_from_elasticapi'),
    bindings=[
        QueueBinding(
            exchange=my_offers_exchange,
            routing_key=OffersResendV1RoutingKey.new.value,
        )
    ],
)

process_announcements_from_temp = Queue(
    name=get_modified_queue_name('process_announcement_from_temp'),
    bindings=_get_bindings('announcements-temp', 'announcement_reporting', AnnouncementReportingV1RoutingKey),
)

save_announcement_contract_queue = Queue(
    name=get_modified_queue_name('save_announcement_contract'),
    bindings=[
        QueueBinding(
            exchange=billing_exchange,
            routing_key=ServiceContractsReportingV1RoutingKey.created.value
        ),
        QueueBinding(
            exchange=billing_exchange,
            routing_key=ServiceContractsReportingV1RoutingKey.changed.value
        )
    ]
)

close_announcement_contract_queue = Queue(
    name=get_modified_queue_name('mark_to_delete_announcement_contract'),
    bindings=[
        QueueBinding(
            exchange=billing_exchange,
            routing_key=ServiceContractsReportingV1RoutingKey.closed.value
        )
    ]
)

save_offer_unload_error_queue = Queue(
    name=get_modified_queue_name('save_offer_unload_error'),
    bindings=[
        QueueBinding(
            exchange=Exchange('unload'),
            routing_key=UnloadOrderReportingV1RoutingKey.error.value
        )
    ]
)

moderation_offence_queue = Queue(
    name=get_modified_queue_name('save_moderation_offer_offence'),
    bindings=[
        QueueBinding(
            exchange=Exchange('moderation'),
            routing_key=ModerationOfferOffenceReportingV1RoutingKey.created.value,
        ),
        QueueBinding(
            exchange=Exchange('moderation'),
            routing_key=ModerationOfferOffenceReportingV1RoutingKey.changed.value,
        )
    ],
)

update_agents_queue = Queue(
    name=get_modified_queue_name('save_agent'),
    bindings=[
        QueueBinding(
            exchange=Exchange('users'),
            routing_key=AgentsReportingV1RoutingKey.updated.value,
        ),
    ],
)

announcement_premoderation_sent_queue = Queue(
    name=get_modified_queue_name('save_offer_premoderation'),
    bindings=[
        QueueBinding(
            exchange=Exchange('moderation'),
            routing_key=AnnouncementPremoderationReportingV1RoutingKey.sent.value,
        ),
    ],
)

announcement_premoderation_remove_queue = Queue(
    name=get_modified_queue_name('remove_offer_premoderation'),
    bindings=[
        QueueBinding(
            exchange=Exchange('moderation'),
            routing_key=AnnouncementPremoderationReportingV1RoutingKey.remove.value,
        ),
    ],
)

update_offer_duplicates_queue = Queue(
    name=get_modified_queue_name('update_offer_duplicates'),
    bindings=[
        QueueBinding(
            exchange=Exchange('ml-ranking-dubli'),
            routing_key='offer.v1.need-update-duplicate',
        ),
    ],
)

new_offer_duplicate_notification_queue = Queue(
    name=get_modified_queue_name('new_offer_duplicate_notification.SNACHEVA'),
    bindings=[
        QueueBinding(
            exchange=my_offers_exchange,
            routing_key=OfferDuplicateV1RoutingKey.new.value,
        ),
    ],
)
