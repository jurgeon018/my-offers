from dataclasses import dataclass


@dataclass
class SubscribeOnDuplicatesRequest:
    email: str
    """Емайл пользователя"""


@dataclass
class UnsubscribeOnDuplicatesRequest:
    email: str
    """Емайл пользователя"""


@dataclass
class NewEmailSubscription:
    user_id: int
    """ID пользователя"""
    email: str
    """Емайл пользователя"""
