# pylint: skip-file
"""

Code generated by new-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client announcementapi`

new-codegen version: 4.0.1

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


class Type(StrEnum):
    __value_format__ = NoFormat
    autonomous = 'autonomous'
    """Автономное"""
    central = 'central'
    """Центральное"""
    pumping_station = 'pumpingStation'
    """Водонапорная станция"""
    water_intake_facility = 'waterIntakeFacility'
    """Водозаборный узел"""
    water_tower = 'waterTower'
    """Водонапорная башня"""


@dataclass
class Water:
    """Водоснабжение"""

    capacity: Optional[int] = None
    """Объём, м³/сутки"""
    locationType: Optional[LocationType] = None
    """Локация водоснабжения"""
    possibleToConnect: Optional[bool] = None
    """Возможно подключить"""
    type: Optional[Type] = None
    """Тип водоснабжения"""
