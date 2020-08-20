from dataclasses import dataclass
from typing import Optional


@dataclass
class SubscribeOnDuplicatesRequest:
    email: str
    """Емайл пользователя"""
    send_mobile_push: Optional[bool] = None
    """Разрешить слать мобильные пуши виесте с подпиской на емайл"""


@dataclass
class SubscribeOnDuplicatesResponse:
    user_already_subscribed: bool
    """Пользователь уже подписан на обновления дубликаотов для объявления"""
