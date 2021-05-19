from datetime import datetime

import pytz
from cian_core.context import get_operation_id
from cian_core.rabbitmq.decorators import mq_producer_v2

from my_offers.helpers.schemas import get_entity_schema
from my_offers.queue.entities import (
    AnnouncementMessage,
    OfferDuplicatePriceChangedMessage,
    OfferNewDuplicateMessage,
    UpdateOfferMasterUserMessage,
)
from my_offers.queue.routing_keys import (
    OfferDuplicateV1RoutingKey,
    OfferMasterUserV1RoutingKey,
    OffersResendV1RoutingKey,
)


async def _get_offer_new_duplicate_message(offer_id: int) -> OfferNewDuplicateMessage:
    return OfferNewDuplicateMessage(
        duplicate_offer_id=offer_id,
        operation_id=get_operation_id(),
        date=datetime.now(tz=pytz.UTC),
    )


async def _get_offer_duplicate_price_changed_message(offer_id: int) -> OfferDuplicatePriceChangedMessage:
    return OfferDuplicatePriceChangedMessage(
        duplicate_offer_id=offer_id,
        operation_id=get_operation_id(),
        date=datetime.now(tz=pytz.UTC),
    )


async def _get_announcement_models(model) -> AnnouncementMessage:
    return AnnouncementMessage(
        model=model,
        operation_id=get_operation_id(),
        date=datetime.now(tz=pytz.UTC),
    )


async def _get_update_offer_master_message(
    *,
    offer_id: int,
    new_master_user_id: int
) -> UpdateOfferMasterUserMessage:
    return UpdateOfferMasterUserMessage(
        offer_id=offer_id,
        new_master_user_id=new_master_user_id,
        operation_id=get_operation_id(),
        date=datetime.now(tz=pytz.UTC),
    )


offer_new_duplicate_producers = mq_producer_v2(
    schema=get_entity_schema(OfferNewDuplicateMessage),
    routing_key=OfferDuplicateV1RoutingKey.new.value,
)(_get_offer_new_duplicate_message)

offer_duplicate_price_changed_producer = mq_producer_v2(
    schema=get_entity_schema(OfferDuplicatePriceChangedMessage),
    routing_key=OfferDuplicateV1RoutingKey.price_changed.value,
)(_get_offer_duplicate_price_changed_message)

announcement_models_producer = mq_producer_v2(
    schema=get_entity_schema(AnnouncementMessage),
    routing_key=OffersResendV1RoutingKey.new.value,
)(_get_announcement_models)

update_offer_master_producer = mq_producer_v2(
    schema=get_entity_schema(UpdateOfferMasterUserMessage),
    routing_key=OfferMasterUserV1RoutingKey.update.value,
)(_get_update_offer_master_message)
