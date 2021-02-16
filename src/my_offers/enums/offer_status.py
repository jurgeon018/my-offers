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


class MobTabType(StrEnum):
    rent = 'rent'
    """Аренда"""
    sale = 'sale'
    """Продажа"""
    archived = 'archived'
    """Архив"""
    inactive = 'inactive'
    "Неактивные"

