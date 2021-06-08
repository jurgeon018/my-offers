from cian_enum import StrEnum


class OfferStatusTab(StrEnum):
    """На какую вкладку поместить объявление"""
    all = 'all'
    """По всем вкладкам"""
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


class OfferStatus(StrEnum):
    xml = 'xml'
    """Импортное объявление"""
    draft = 'draft'
    """Черновик"""


class MobTabTypeV1(StrEnum):
    rent = 'rent'
    """Аренда"""
    sale = 'sale'
    """Продажа"""
    archived = 'archived'
    """Архив"""
    inactive = 'inactive'
    """Неактивные (declined + not_active)"""


class MobTabTypeV2(StrEnum):
    rent = 'rent'
    """Аренда"""
    sale = 'sale'
    """Продажа"""
    archived = 'archived'
    """Архив"""
    inactive = 'inactive'
    """Неактивные"""
    declined = 'declined'
    """Отклоненные модерацией"""


# аналог src/my_offers/repositories/monolith_cian_announcementapi/entities/object_model.py
# только с маленькой буквы
class MobStatus(StrEnum):
    draft = 'draft'
    """Черновик"""
    published = 'published'
    """Опубликовано"""
    deactivated = 'deactivated'
    """Деактивировано (ранее было скрыто Hidden)"""
    refused = 'refused'
    """Отклонено модератором"""
    deleted = 'deleted'
    """Удалён"""
    sold = 'sold'
    """Продано/Сдано"""
    moderate = 'moderate'
    'Требует модерации\r\nДанный статус исчез - оставим для совместимости'
    removed_by_moderator = 'removedByModerator'
    """Удалено модератором"""
    blocked = 'blocked'
    """объявление снято с публикации по причине применения санкции "приостановки публикации\""""
