from cian_enum import NoFormat, StrEnum


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
