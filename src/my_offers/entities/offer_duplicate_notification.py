from dataclasses import dataclass
from datetime import datetime

from my_offers.enums.notifications import UserNotificationType


@dataclass
class OfferDuplicateNotification:
    offer_id: int
    """Id объявления"""
    duplicate_offer_id: int
    """Id объявления дубликата"""
    send_at: datetime
    """Дата отправления душа"""
    notification_type: UserNotificationType
    """Тип уведомления"""
