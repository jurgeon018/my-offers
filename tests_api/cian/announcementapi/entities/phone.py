# pylint: skip-file
"""

Code generated by new-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client announcementapi`

new-codegen version: 4.0.0

"""
from dataclasses import dataclass
from typing import Optional

from .source_phone import SourcePhone


@dataclass
class Phone:
    countryCode: str
    """Код страны"""
    number: str
    """Номер"""
    sourcePhone: Optional[SourcePhone] = None
    """Исходный номер телефона"""
