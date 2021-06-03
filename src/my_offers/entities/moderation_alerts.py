from dataclasses import dataclass

from cian_enum import StrEnum


class TabType(StrEnum):
    rent = 'rent'
    """Аренда"""
    sale = 'sale'
    """Продажа"""
    archived = 'archived'
    """Архив"""
    inactive = 'inactive'
    """Неактивные"""
    declined = 'declined'
    """Отклоненные"""


@dataclass
class HideWarningsRequest:
    tab_type: TabType
