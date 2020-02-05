from cian_enum import StrEnum


class GetOfferType(StrEnum):
    """Тип недвижимости"""
    flat = 'flat'
    """Жилая"""
    suburban = 'suburban'
    """Загородная"""
    commercial = 'commercial'
    """Коммерческая"""


class OfferType(StrEnum):
    """Тип недвижимости"""
    flat = 'flat'
    """Жилая"""
    newobject = 'newobject'
    """Новостройки"""
    suburban = 'suburban'
    """Загородная"""
    commercial = 'commercial'
    """Коммерческая"""
