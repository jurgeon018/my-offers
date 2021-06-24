# pylint: skip-file
"""

Code generated by cian-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client monolith-cian-announcementapi`

cian-codegen version: 1.15.0

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


@dataclass
class Electricity:
    """Электричество"""

    location_type: Optional[LocationType] = None
    """Локация электроснабжения"""
    possible_to_connect: Optional[bool] = None
    """Возможно подключить"""
    power: Optional[int] = None
    """Мощность, кВТ"""
