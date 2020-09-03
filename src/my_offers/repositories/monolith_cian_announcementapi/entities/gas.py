# pylint: skip-file
"""

Code generated by cian-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client monolith-cian-announcementapi`

cian-codegen version: 1.5.0

"""
from dataclasses import dataclass
from typing import Optional

from cian_enum import NoFormat, StrEnum


class LocationType(StrEnum):
    __value_format__ = NoFormat
    no = 'no'
    """Нет"""
    border = 'border'
    """По границе участка"""
    location = 'location'
    """На участке"""


class PressureType(StrEnum):
    __value_format__ = NoFormat
    high = 'high'
    """Высокое"""
    middle = 'middle'
    """Среднее"""
    low = 'low'
    """Низкое"""


@dataclass
class Gas:
    """Газоснабжение"""

    capacity: Optional[int] = None
    """Ёмкость, м³/час"""
    location_type: Optional[LocationType] = None
    """Локация газоснабжения"""
    possible_to_connect: Optional[bool] = None
    """Возможно подключить"""
    pressure_type: Optional[PressureType] = None
    """Давление"""
