from cian_core.context import get_operation_id
from cian_core.kafka import get_kafka_entity_producer
from cian_kafka import EntityKafkaProducer

from my_offers.queue import enums
from my_offers.queue.entities import OfferDuplicateEvent
from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel


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
    def produce_new_duplicate_event(cls, *, offer: ObjectModel, duplicate_offer: ObjectModel) -> None:
        instance = cls._instance()
        message = OfferDuplicateEvent(
            user_id=offer.published_user_id,
            event_type=enums.PushType.push_offer_duplicate,
            object_id=offer.id,
            similar_object_id=duplicate_offer.id,
            # similar_object_price: int
            # """цена объявки-дубля в рублях"""
            # region_id: int
            # """id региона, в котором публикуется объявление-дубль или меняется цена на него"""
            operation_id=get_operation_id(),
        )
        instance(message)
