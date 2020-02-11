# pylint: skip-file
"""

Code generated by new-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client announcementapi`

new-codegen version: 4.0.0

"""
from dataclasses import dataclass
from typing import Optional

from .booking import Booking


@dataclass
class Flat:
    booking: Optional[Booking] = None
    """Бронирование квартиры"""
    flatNumber: Optional[int] = None
    """Номер на площадке"""
    flatType: Optional[str] = None
    """Тип квартиры"""
    sectionNumber: Optional[str] = None
    """Номер секции"""
