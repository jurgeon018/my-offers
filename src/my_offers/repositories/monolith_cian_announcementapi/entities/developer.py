# pylint: skip-file
"""

Code generated by cian-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client monolith-cian-announcementapi`

cian-codegen version: 1.9.0

"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Developer:
    """Застройщик"""

    id: Optional[int] = None
    """ID застройщика"""
    name: Optional[str] = None
    """Название"""
