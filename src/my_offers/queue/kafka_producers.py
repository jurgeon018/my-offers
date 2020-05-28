from cian_core.kafka import get_kafka_entity_producer
from cian_kafka import EntityKafkaProducer

from my_offers.entities.offer_duplicate_notification import OfferDuplicateEvent


class OfferDuplicateEventProducer:
    __instance = None

    @classmethod
    def _instance(cls) -> EntityKafkaProducer[OfferDuplicateEvent]:
        if not cls.__instance:
            cls.__instance = get_kafka_entity_producer(
                topic='myoffer-specialist-push-notification',
                message_type=OfferDuplicateEvent,
            )

        return cls.__instance

    @classmethod
    def produce(cls, message: OfferDuplicateEvent):
        instance = cls._instance()
        instance(message)
