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


@dataclass
class HasUnreadWarningsRequest:
    user_id: int
    """ID пользователя"""


@dataclass
class HasUnreadWarningsResponse:
    has_warnings: bool
    """Наличие непросмотренных нарушений модерации"""
