# pylint: skip-file
"""

Code generated by new-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client announcementapi`

new-codegen version: 4.0.0

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

    locationType: Optional[LocationType] = None
    """Локация электроснабжения"""
    possibleToConnect: Optional[bool] = None
    """Возможно подключить"""
    power: Optional[int] = None
    """Мощность, кВТ"""