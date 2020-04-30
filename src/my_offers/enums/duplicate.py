from cian_enum import StrEnum


class DuplicateTabType(StrEnum):
    all = 'all'
    """Все сразу"""
    duplicate = 'duplicate'
    """Дубликат объявления"""


class DuplicateType(StrEnum):
    duplicate = 'duplicate'
    """Дубликат объявления"""
