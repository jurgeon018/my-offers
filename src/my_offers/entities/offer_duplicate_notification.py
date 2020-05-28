from dataclasses import dataclass
from datetime import datetime


@dataclass
class OfferDuplicateNotification:
    offer_id: int
    """Id объявления"""
    duplicate_offer_id: int
    """Id объявления дубликата"""
    send_at: datetime
    """Дата отправления душа"""


@dataclass
class OfferDuplicateEvent:
    user_id: int
    """realtyUserId пользователя"""
