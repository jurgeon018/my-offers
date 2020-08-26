from cian_enum import StrEnum


class UserNotificationType(StrEnum):
    mobile_push = 'mobile_push'
    """Мобильный пуш"""
    email_push = 'email_push'
    """Почтовое уведомление"""
