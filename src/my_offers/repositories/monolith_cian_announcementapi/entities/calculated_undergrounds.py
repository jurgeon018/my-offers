# pylint: skip-file
"""

Code generated by cian-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client monolith-cian-announcementapi`

cian-codegen version: 1.4.1

"""
from dataclasses import dataclass
from typing import Optional

from cian_enum import NoFormat, StrEnum


class TransportType(StrEnum):
    __value_format__ = NoFormat
    transport = 'transport'
    """На транспорте"""
    walk = 'walk'
    """Пешком"""


@dataclass
class CalculatedUndergrounds:
    """Автоматически рассчитанное время в пути до станции метро"""

    distance: Optional[int] = None
    """Расстояние до метро, метры"""
    id: Optional[int] = None
    """Id метро"""
    time: Optional[int] = None
    """Время в пути в минутах до метро, мин"""
    transport_type: Optional[TransportType] = None
    """Способ передвижения до метро"""
