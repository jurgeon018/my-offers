# pylint: skip-file
"""

Code generated by cian-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client monolith-cian-announcementapi`

cian-codegen version: 1.9.0

"""
from dataclasses import dataclass
from typing import List, Optional

from cian_enum import NoFormat, StrEnum

from .announcement_progress_dto import AnnouncementProgressDto


class State(StrEnum):
    __value_format__ = NoFormat
    new = 'New'
    """Новое"""
    in_progress = 'InProgress'
    """В обработке"""
    completed = 'Completed'
    """Завершено"""
    error = 'Error'
    """Завершено с ошибками"""


@dataclass
class GetJobStatusResponse:
    """Статус выполнения задачи"""

    state: State
    """Статус задачи."""
    announcements_progress: Optional[List[AnnouncementProgressDto]] = None
    """Статусы объявлений."""
