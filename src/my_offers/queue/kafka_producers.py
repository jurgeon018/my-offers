from cian_core.kafka import get_kafka_entity_producer
from cian_kafka import EntityKafkaProducer

from my_offers.entities.offer_duplicate_notification import OfferDuplicateEvent

offer_duplicate_event_producer = get_kafka_entity_producer(
    topic='myoffer-specialist-push-notification',
    message_type=OfferDuplicateEvent,
)


class OfferDuplicateEventProducer:
    __instance = None

    @classmethod
    def instance(cls) -> EntityKafkaProducer[OfferDuplicateEvent]:
        if not cls.__instance:
            cls.__instance = get_kafka_entity_producer(
                topic='myoffer-specialist-push-notification',
                message_type=OfferDuplicateEvent,
            )

        return cls.__instance
