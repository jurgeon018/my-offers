from my_offers.entities import OfferSimilar
from my_offers.enums.notifications import DuplicateNotificationType
from my_offers.helpers.category import get_types
from my_offers.helpers.fields import get_main_photo_url
from my_offers.helpers.numbers import get_pretty_number
from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel
from my_offers.repositories.notification_center import v2_register_notifications
from my_offers.repositories.notification_center.entities import (
    RegisterNotificationV2Request,
    RegisterNotificationsV2Request,
)
from my_offers.repositories.notification_center.entities.register_notification_v2_request import (
    NotificationType,
    TransportsToSend,
)
from my_offers.services.notifications.push_enabled import is_mobile_push_enabled
from my_offers.services.offer_view import fields
from my_offers.services.offer_view.fields.geo import get_address_for_push


async def send_duplicate_price_changed_mobile_push(
        *,
        user_id: int,
        offer: ObjectModel,
        duplicate_offer: ObjectModel,
        duplicate_similar: OfferSimilar,
) -> None:
    """ Послать мобильный пуш об изменении цены в дубле"""

    offer_type, deal_type = get_types(offer.category)

    if await is_mobile_push_enabled(user_id=user_id, push_type=DuplicateNotificationType.price_changed):
        await v2_register_notifications(
            RegisterNotificationsV2Request(
                notifications=[RegisterNotificationV2Request(
                    notification_type=NotificationType.duplicate_price_changed,
                    is_authenticated=True,
                    user_id=str(user_id),
                    entity_id=offer.id,
                    mobile_push_payload={
                        'dealType': deal_type.value,
                        'offerType': offer_type.value,
                        'priceChangeButtonText': 'Изменить мою цену'
                    },
                    text=get_address_for_push(offer.geo),
                    title=get_title(duplicate_similar=duplicate_similar),
                    web_url=fields.get_offer_url(
                        cian_offer_id=duplicate_offer.cian_id,
                        offer_type=offer_type,
                        deal_type=deal_type
                    ),
                    media_url=get_main_photo_url(offer.photos),
                    transports_to_send=[TransportsToSend.mobile_push],
                )]
            )
        )


def get_title(*, duplicate_similar: OfferSimilar) -> str:
    title = ''
    if duplicate_similar.price > duplicate_similar.old_price:
        title += 'Цена на дубль увеличена'
    else:
        title += 'Цена на дубль снижена'
    title += f' до\xa0{get_pretty_number(duplicate_similar.price)}\xa0₽'

    return title
