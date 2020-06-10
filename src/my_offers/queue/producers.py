from datetime import datetime

import pytz
from cian_core.context import get_operation_id
from cian_core.rabbitmq.decorators import mq_producer_v2

from my_offers.helpers.schemas import get_entity_schema
from my_offers.queue.entities import AnnouncementMessage, OfferNewDuplicateMessage
from my_offers.queue.routing_keys import OfferDuplicateV1RoutingKey, OffersResendV1RoutingKey


async def _get_offer_new_duplicate_message(offer_id: int) -> OfferNewDuplicateMessage:
    return OfferNewDuplicateMessage(
        duplicate_offer_id=offer_id,
        operation_id=get_operation_id(),
        date=datetime.now(tz=pytz.UTC),
    )


async def _get_announcement_models(model):
    return AnnouncementMessage(
        model=model,
        operation_id=get_operation_id(),
        date=datetime.now(tz=pytz.UTC),
    )


offer_new_duplicate_producers = mq_producer_v2(
    schema=get_entity_schema(OfferNewDuplicateMessage),
    routing_key=OfferDuplicateV1RoutingKey.new.value,
)(_get_offer_new_duplicate_message)

announcement_models_producer = mq_producer_v2(
    schema=get_entity_schema(AnnouncementMessage),
    routing_key=OffersResendV1RoutingKey.new.value,
)(_get_announcement_models)
