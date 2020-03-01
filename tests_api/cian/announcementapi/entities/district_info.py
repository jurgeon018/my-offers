# pylint: skip-file
"""

Code generated by new-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client announcementapi`

new-codegen version: 4.0.1

"""
from dataclasses import dataclass
from typing import Optional

from cian_enum import NoFormat, StrEnum


class Type(StrEnum):
    __value_format__ = NoFormat
    okrug = 'okrug'
    """Административный округ"""
    raion = 'raion'
    """Район"""
    mikroraion = 'mikroraion'
    """Микрорайон"""
    poselenie = 'poselenie'
    """Административный округ"""


@dataclass
class DistrictInfo:
    id: Optional[int] = None
    """ID района"""
    locationId: Optional[int] = None
    """ID гео-привязки"""
    name: Optional[str] = None
    """Название"""
    parentId: Optional[int] = None
    """ID родительского района"""
    type: Optional[Type] = None
    """Тип района"""
