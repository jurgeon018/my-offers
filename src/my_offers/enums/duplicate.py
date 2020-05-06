from cian_enum import StrEnum


class PriceTrend(StrEnum):
    inc = 'inc'
    """Увеличилась"""
    dec = 'dec'
    """Уменьшилась"""


class DuplicateTabType(StrEnum):
    all = 'all'
    """Все сразу"""
    duplicate = 'duplicate'
    """Дубликат объявления"""


class DuplicateType(StrEnum):
    duplicate = 'duplicate'
    """Дубликат объявления"""
