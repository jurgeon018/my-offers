# pylint: skip-file
"""

Code generated by new-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client announcementapi`

new-codegen version: 4.0.0

"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Coordinates:
    lat: Optional[float] = None
    """Широта"""
    lng: Optional[float] = None
    """Долгота"""