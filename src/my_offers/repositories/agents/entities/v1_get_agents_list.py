# pylint: skip-file
"""

Code generated by cian-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client agents`

cian-codegen version: 1.15.1

"""
from dataclasses import dataclass
from typing import List, Optional

from cian_enum import NoFormat, StrEnum


class Statuses(StrEnum):
    __value_format__ = NoFormat
    request = 'request'
    """Отправлена заявка на добавление агента к агентству"""
    active = 'active'
    """Активный агент"""
    processing = 'processing'
    """Агент в процессе активации/блокировки"""
    blocked = 'blocked'
    """Заблокированный агент"""
    deleted = 'deleted'
    """Удаленный агент"""
    deleted_and_hidden = 'deletedAndHidden'
    """Удаленный агент"""


@dataclass
class V1GetAgentsList:
    page: int
    """Номер запрашиваемой страницы."""
    page_size: int
    """Размер страницы."""
    user_id: int
    """Id пользователя - мастер-агента."""
    query: Optional[str] = None
    """Поисковый запрос"""
    statuses: Optional[List[Statuses]] = None
    """Статусы"""
    user_ids: Optional[List[int]] = None
    """Список сотрудников, которых нужно вернуть в ответе. Если не задан - вернуть информацию по всем сотрудникам."""
