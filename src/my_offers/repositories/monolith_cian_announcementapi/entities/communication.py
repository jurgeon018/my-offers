# pylint: skip-file
"""

Code generated by cian-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client monolith-cian-announcementapi`

cian-codegen version: 1.15.0

"""
from dataclasses import dataclass
from typing import Optional

from cian_enum import NoFormat, StrEnum


class PreferredCommunicationType(StrEnum):
    __value_format__ = NoFormat
    phone = 'phone'
    """По телефону"""
    forms = 'forms'
    """С помощью анкет"""


@dataclass
class Communication:
    """Виды коммуникаций с пользователями"""

    preferred_communication_type: Optional[PreferredCommunicationType] = None
    """Предпочитаемый тип связи"""
