from cian_enum import NoFormat, StrEnum


class UserNotificationType(StrEnum):
    mobile_push = 'mobile_push'
    """Мобильный пуш"""
    email_push = 'email_push'
    """Почтовое уведомление"""


class DuplicateNotificationType(StrEnum):
    __value_format__ = NoFormat
    new_duplicate = 'OfferNewDuplicateFoundNotifications'
    """Уведомление о новом дубле"""
    price_changed = 'DuplicatePriceChangedNotifications'
    """Увеедомление об изменении цены дубля"""
