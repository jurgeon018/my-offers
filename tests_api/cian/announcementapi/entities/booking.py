# pylint: skip-file
"""

Code generated by new-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client announcementapi`

new-codegen version: 4.0.0

"""
from dataclasses import dataclass
from typing import Optional

from cian_enum import NoFormat, StrEnum


class Status(StrEnum):
    __value_format__ = NoFormat
    free = 'free'
    """Свободна."""
    in_reserve = 'inReserve'
    """В резерве."""


@dataclass
class Booking:
    """Бронирование."""

    cost: Optional[int] = None
    """Стоимость бронирования."""
    status: Optional[Status] = None
    """Статус бронирования."""
