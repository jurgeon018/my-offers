from typing import Optional

from cian_core.context import get_operation_id
from cian_core.kafka import get_kafka_entity_producer
from cian_kafka import EntityKafkaProducer

from my_offers.enums.notifications import UserNotificationType
from my_offers.helpers.fields import get_locations
from my_offers.queue import enums
from my_offers.queue.entities import OfferDuplicateEvent
from my_offers.repositories.monolith_cian_announcementapi.entities import Geo, ObjectModel


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
    async def produce_new_duplicate_event(
            cls, *,
            offer: ObjectModel,
            duplicate_offer: ObjectModel,
            transport_type: UserNotificationType
    ) -> None:
        instance = cls._instance()

        message = OfferDuplicateEvent(
            user_id=offer.published_user_id,
            event_type=enums.PushType.push_offer_duplicate,
            object_id=offer.id,
            similar_object_id=duplicate_offer.id,
            similar_object_price=duplicate_offer.bargain_terms.price if duplicate_offer.bargain_terms else None,
            region_id=cls._get_region_id(duplicate_offer.geo),
            operation_id=get_operation_id(),
            transport=transport_type
        )
        await instance(message)

    @classmethod
    def _get_region_id(cls, geo: Optional[Geo]) -> Optional[int]:
        if locations := get_locations(geo):
            result = locations[-1]
        else:
            result = None

        return result
