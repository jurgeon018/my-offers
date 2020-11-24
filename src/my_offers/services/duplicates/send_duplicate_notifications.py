import logging

from my_offers.enums.notifications import UserNotificationType
from my_offers.queue.enums import PushType
from my_offers.queue.kafka_producers import OfferDuplicateEventProducer
from my_offers.repositories.postgresql.object_model import get_object_model
from my_offers.repositories.postgresql.offers_duplicates import get_offer_duplicates
from my_offers.repositories.postgresql.offers_similars import get_offer_similar
from my_offers.services.notifications import send_new_duplicates_notification
from my_offers.services.notifications.price_changed_duplicate_notification import (
    send_duplicate_price_changed_mobile_push,
)
from my_offers.services.similars.helpers.table import get_similar_table_suffix


logger = logging.getLogger(__name__)


async def send_new_duplicate_notifications(duplicate_offer_id: int) -> None:
    """ Послать уведомляние по новому дубликату объявления"""
    limit = 100
    offset = 0

    duplicate_offer = await get_object_model({'offer_id': duplicate_offer_id})
    if not duplicate_offer or not duplicate_offer.status.is_published:
        return

    while True:
        duplicates = await get_offer_duplicates(
            offer_id=duplicate_offer_id,
            limit=limit,
            offset=offset,
        )
        offset += limit
        if not duplicates:
            break

        for offer, _ in duplicates:
            user_id = offer.published_user_id
            if user_id == duplicate_offer.published_user_id:
                continue

            await send_new_duplicates_notification(
                offer=offer,
                duplicate_offer=duplicate_offer,
                user_id=user_id
            )


async def send_duplicate_price_changed_notifications(duplicate_offer_id: int) -> None:
    """ Послать уведомляние об изменении цены дубликата объявления"""
    limit = 100
    offset = 0

    duplicate_offer = await get_object_model({'offer_id': duplicate_offer_id})
    if not duplicate_offer or not duplicate_offer.status.is_published:
        return

    duplicate_from_similar = await get_offer_similar(
        offer_id=duplicate_offer_id,
        suffix=get_similar_table_suffix(duplicate_offer)
    )
    if not duplicate_from_similar or not duplicate_from_similar.old_price:
        return

    if abs(duplicate_from_similar.price - duplicate_from_similar.old_price) < 1:
        logger.warning('DuplicatePriceChangeError: Price changed less 1rub, old_price: %s, new_price: %s',
                       duplicate_from_similar.old_price, duplicate_from_similar.price)
        return

    while True:
        duplicates = await get_offer_duplicates(
            offer_id=duplicate_offer_id,
            limit=limit,
            offset=offset,
        )
        offset += limit
        if not duplicates:
            break

        for offer, _ in duplicates:
            user_id = offer.published_user_id
            if user_id == duplicate_offer.published_user_id:
                continue

            await send_duplicate_price_changed_mobile_push(
                offer=offer,
                duplicate_offer=duplicate_offer,
                duplicate_similar=duplicate_from_similar,
                user_id=user_id
            )

            await OfferDuplicateEventProducer.produce_duplicate_event(
                offer=offer,
                duplicate_offer=duplicate_offer,
                transport_type=UserNotificationType.mobile_push,
                event_type=PushType.push_price_change_offer_duplicate,
            )
