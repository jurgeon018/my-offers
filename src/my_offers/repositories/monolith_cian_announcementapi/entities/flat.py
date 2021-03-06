# pylint: skip-file
"""

Code generated by cian-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client monolith-cian-announcementapi`

cian-codegen version: 1.15.0

"""
from dataclasses import dataclass
from typing import Optional

from .booking import Booking


@dataclass
class Flat:
    booking: Optional[Booking] = None
    """Бронирование квартиры"""
    flat_number: Optional[int] = None
    """Номер на площадке"""
    flat_type: Optional[str] = None
    """Тип квартиры"""
    section_number: Optional[str] = None
    """Номер секции"""
