from cian_enum import NoFormat, StrEnum


class OfferStatus(StrEnum):
    __value_format__ = NoFormat
    draft = 'Draft'
    """11 - Черновик"""
    published = 'Published'
    """12 - Опубликовано"""
    deactivated = 'Deactivated'
    """14 - Деактивировано (ранее было скрыто Hidden)"""
    refused = 'Refused'
    """15 - Отклонено модератором"""
    deleted = 'Deleted'
    """16 - Удалён"""
    sold = 'Sold'
    """17 - Продано/Сдано"""
    moderate = 'Moderate'
    '18 - Требует модерации\r\nДанный статус исчез - оставим для совместимости'
    removed_by_moderator = 'RemovedByModerator'
    """19 - Удалено модератором"""
    blocked = 'Blocked'
    """20 - объявление снято с публикации по причине применения санкции "приостановки публикации\""""


class GetOfferStatusTab(StrEnum):
    """На какую вкладку поместить объявление"""
    active = 'active'
    """Активные"""
    not_active = 'not_active'
    """Неактивные"""
    declined = 'declined'
    """Отклоненные"""
    archived = 'archived'
    """Архив"""


class OfferStatusTab(StrEnum):
    __value_format__ = NoFormat
    """На какую вкладку поместить объявление"""
    active = 'active'
    """Активные"""
    not_active = 'not_active'
    """Неактивные"""
    declined = 'declined'
    """Отклоненные"""
    archived = 'archived'
    """Архив"""
    deleted = 'deleted'
    """Удалено"""
