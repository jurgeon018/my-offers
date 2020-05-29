from datetime import datetime

import pytz
from asyncpg import UniqueViolationError

from my_offers.entities.offer_duplicate_notification import OfferDuplicateNotification
from my_offers.helpers.category import get_types
from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel
from my_offers.repositories.notification_center import v2_register_notifications
from my_offers.repositories.notification_center.entities import (
    RegisterNotificationsV2Request,
    RegisterNotificationV2Request,
)
from my_offers.repositories.notification_center.entities.register_notification_v2_request import (
    NotificationType,
    TransportsToSend,
)
from my_offers.repositories.postgresql.object_model import get_object_model
from my_offers.repositories.postgresql.offers_duplicate_notification import (
    delete_offers_duplicate_notification,
    save_offers_duplicate_notification,
)
from my_offers.repositories.postgresql.offers_duplicates import get_offer_duplicates
from my_offers.services.offer_view.fields import get_main_photo_url, get_offer_url
from my_offers.services.offer_view.fields.geo import get_address_for_push


async def send_new_offer_duplicate_notifications(duplicate_offer_id: int) -> None:
    limit = 100
    offset = 0

    duplicate_offer = await get_object_model({'offer_id': duplicate_offer_id})
    if not duplicate_offer or not duplicate_offer.status.is_published:
        return

    while True:
        duplicates, _ = await get_offer_duplicates(
            offer_id=duplicate_offer_id,
            limit=limit,
            offset=offset,
        )
        offset += limit
        if not duplicates:
            break

        for offer in duplicates:
            if offer.published_user_id == duplicate_offer.published_user_id:
                continue

            await process_notification(offer=offer, duplicate_offer=duplicate_offer)


async def process_notification(*, offer: ObjectModel, duplicate_offer: ObjectModel) -> None:
    notification = OfferDuplicateNotification(
        offer_id=offer.id,
        duplicate_offer_id=duplicate_offer.id,
        send_at=datetime.now(tz=pytz.utc)
    )

    try:
        await save_offers_duplicate_notification(notification)
    except UniqueViolationError:
        # уже отправляли
        return

    try:
        await _send_notification(offer)
    except:
        # неполучилось отправить
        await delete_offers_duplicate_notification(notification)
        raise

    # todo: https://jira.cian.tech/browse/CD-81714 отправить событие для МЛ


async def _send_notification(offer: ObjectModel):
    offer_type, deal_type = get_types(offer.category)

    await v2_register_notifications(RegisterNotificationsV2Request(
        notifications=[RegisterNotificationV2Request(
            notification_type=NotificationType.offer_new_duplicate_found,
            is_authenticated=True,
            user_id=str(offer.published_user_id),
            entity_id=offer.id,
            mobile_push_payload={
                'dealType': deal_type.value,
                'offerType': offer_type.value,
            },
            text=get_address_for_push(offer.geo),
            title='Новый дубль вашего объекта',
            web_url=get_offer_url(offer_id=offer.id, offer_type=offer_type, deal_type=deal_type),
            media_url=get_main_photo_url(offer.photos),
            transports_to_send=[TransportsToSend.mobile_push],
        )]
    ))
