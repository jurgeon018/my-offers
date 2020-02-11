from cian_enum import StrEnum


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
