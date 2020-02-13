from cian_enum import StrEnum


class AddressType(StrEnum):
    country = 'country'
    """Страна"""
    district = 'district'
    """Район"""
    house = 'house'
    """Дом"""
    location = 'location'
    """Местоположение"""
    road = 'road'
    """Шоссе"""
    street = 'street'
    """Улица"""
    underground = 'underground'
    """Метро"""
