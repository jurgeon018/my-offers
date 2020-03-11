# pylint: skip-file
"""

Code generated by new-codegen; DO NOT EDIT.

To re-generate, run `new-codegen generate-client announcementapi`

new-codegen version: 4.0.2

"""
from dataclasses import dataclass
from typing import Optional

from cian_enum import NoFormat, StrEnum


class Quarter(StrEnum):
    __value_format__ = NoFormat
    first = 'first'
    """Первый"""
    second = 'second'
    """Второй"""
    third = 'third'
    """Третий"""
    fourth = 'fourth'
    """Четвертый"""


@dataclass
class Deadline:
    isComplete: Optional[bool] = None
    """Дом сдан"""
    quarter: Optional[Quarter] = None
    """Квартал"""
    year: Optional[int] = None
    """Срок сдачи"""
