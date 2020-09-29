import asyncio
import logging
from datetime import datetime
from typing import List, Optional

import pytz
from asyncpg import UniqueViolationError
from cian_json import json
from simple_settings import settings

from my_offers.entities.offer_duplicate_notification import OfferDuplicateNotification
from my_offers.enums.notifications import UserNotificationType
from my_offers.helpers.category import get_types
from my_offers.helpers.fields import get_main_photo_url
from my_offers.helpers.title import get_offer_title, SQUARE_METER_SYMBOL
from my_offers.queue.kafka_producers import OfferDuplicateEventProducer
from my_offers.repositories import postgresql
from my_offers.repositories.emails import emails_v2_send_email
from my_offers.repositories.emails.entities import SendEmailByEmailRequest, SendEmailByEmailResponse
from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel
from my_offers.repositories.notification_center import v1_mobile_push_get_settings, v2_register_notifications
from my_offers.repositories.notification_center.entities import (
    GetMobilePushSettingsRequest,
    GetMobilePushSettingsResponse,
    RegisterNotificationsV2Request,
    RegisterNotificationV2Request,
)
from my_offers.repositories.notification_center.entities.get_mobile_push_settings_request import OsType
from my_offers.repositories.notification_center.entities.register_notification_v2_request import (
    NotificationType,
    TransportsToSend,
)
from my_offers.services.offer_view import fields
from my_offers.services.offer_view.fields.geo import get_address_for_push


logger = logging.getLogger(__name__)

SQUARE_METER_SYMBOL_FOR_EMAIL = 'м&sup2;'

async def send_duplicates_notification(
        *,
        user_id: int,
        offer: ObjectModel,
        duplicate_offer: ObjectModel,
) -> None:
    """ Отправить уведомление по дубликату пользователю """
    available_notifications = await get_notification_types(user_id=user_id)

    for notification_type in available_notifications:
        notification = OfferDuplicateNotification(
            offer_id=offer.id,
            duplicate_offer_id=duplicate_offer.id,
            send_at=datetime.now(tz=pytz.utc),
            notification_type=notification_type
        )

        try:
            await postgresql.save_offers_duplicate_notification(notification)
        except UniqueViolationError:
            # уже отправляли
            continue

        try:
            if notification_type.is_email_push:
                email = await postgresql.get_user_email(user_id=user_id)
                await send_email_duplicate_notification(
                    email=email,
                    offer=offer,
                    duplicate_offer=duplicate_offer
                )
            elif notification_type.is_mobile_push:
                await send_mobile_duplicate_notification(
                    user_id=offer.published_user_id,
                    offer=offer,
                    duplicate_offer=duplicate_offer
                )
            else:
                logger.warning('Unsupported notification type: %s', notification_type)
                return
        except Exception:
            # неполучилось отправить
            await postgresql.delete_offers_duplicate_notification(notification)
            raise

        await OfferDuplicateEventProducer.produce_new_duplicate_event(
            offer=offer,
            duplicate_offer=duplicate_offer,
            transport_type=notification_type
        )


async def send_email_duplicate_notification(
        *,
        email: Optional[str],
        offer: ObjectModel,
        duplicate_offer: ObjectModel,
) -> None:
    """ Послать почтовое уведомление на почту пользователя по дублю объявления """
    if not email:
        return

    offer_type, deal_type = get_types(offer.category)
    offer_name = get_offer_title(object_model=offer).replace(SQUARE_METER_SYMBOL, SQUARE_METER_SYMBOL_FOR_EMAIL)
    offer_url = fields.get_offer_url(cian_offer_id=offer.cian_id, offer_type=offer_type, deal_type=deal_type)
    offer_duplicate_name = get_offer_title(object_model=duplicate_offer)
    offer_duplicate_url = fields.get_offer_url(
        cian_offer_id=duplicate_offer.cian_id,
        offer_type=offer_type,
        deal_type=deal_type
    )

    # параметры чувствительны к регистру
    parameters = {
        'ObjectName': offer_name,
        'ObjectLink': offer_url,
        'DoubleObject': offer_duplicate_name,
        'DoubleObjectLink': offer_duplicate_url,
        'UnsubscribeLetter': settings.EMAIL_UNSUBSCRIBE_URL
    }

    response: SendEmailByEmailResponse = await emails_v2_send_email(
        SendEmailByEmailRequest(
            address_list=[email],
            template_name=settings.EMAIL_DUPLICATE_TEMPLATE,
            parameters=json.dumps(parameters)
        ))

    if response.status and response.status.is_user_not_found:
        logger.error('User not found in `emails` service')


async def send_mobile_duplicate_notification(
        *,
        user_id: int,
        offer: ObjectModel,
        duplicate_offer: ObjectModel,
) -> None:
    """ Послать мобильное уведомление по дублю объявления """

    offer_type, deal_type = get_types(offer.category)

    await v2_register_notifications(
        RegisterNotificationsV2Request(
            notifications=[RegisterNotificationV2Request(
                notification_type=NotificationType.offer_new_duplicate_found,
                is_authenticated=True,
                user_id=str(user_id),
                entity_id=offer.id,
                mobile_push_payload={
                    'dealType': deal_type.value,
                    'offerType': offer_type.value,
                    'duplicateOfferId': duplicate_offer.id,
                },
                text=get_address_for_push(offer.geo),
                title='Новый дубль вашего объекта',
                web_url=fields.get_offer_url(
                    cian_offer_id=duplicate_offer.cian_id,
                    offer_type=offer_type,
                    deal_type=deal_type
                ),
                media_url=get_main_photo_url(offer.photos),
                transports_to_send=[TransportsToSend.mobile_push],
            )]
        ))


async def get_notification_types(user_id: int) -> List[UserNotificationType]:
    """ Получить доступные типы уведомлений для пользователя """

    mobile_push, email_push = await asyncio.gather(
        _is_mobile_push_enabled(user_id=user_id),
        _is_email_push_enabled(user_id=user_id),
    )
    notifications = []

    if mobile_push:
        notifications.append(UserNotificationType.mobile_push)
    if email_push:
        notifications.append(UserNotificationType.email_push)

    return notifications


async def _is_mobile_push_enabled(user_id: int) -> bool:
    response: GetMobilePushSettingsResponse = await v1_mobile_push_get_settings(
        GetMobilePushSettingsRequest(
            user_id=str(user_id),
            is_authenticated=True,
            os_type=OsType.android,
        ))

    for item in response.items:
        for child_item in item.children:
            if child_item.id == 'OfferNewDuplicateFoundNotifications':
                return child_item.is_active

    return False


async def _is_email_push_enabled(user_id: int) -> bool:
    return await postgresql.is_any_subscriptions_exists(user_id=user_id)
