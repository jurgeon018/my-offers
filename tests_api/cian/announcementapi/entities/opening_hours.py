# pylint: skip-file
"""

Code generated by new-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client announcementapi`

new-codegen version: 4.0.0

"""
from dataclasses import dataclass
from typing import Optional

from cian_enum import NoFormat, StrEnum


class Type(StrEnum):
    __value_format__ = NoFormat
    round_the_clock = 'roundTheClock'
    """Круглосуточно"""
    specific = 'specific'
    """От/до"""


@dataclass
class OpeningHours:
    """Часы работы"""

    from_: Optional[str] = None
    """От"""
    to: Optional[str] = None
    """До"""
    type: Optional[Type] = None
    """От/до или круглосуточно"""
