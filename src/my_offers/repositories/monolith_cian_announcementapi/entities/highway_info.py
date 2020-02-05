# pylint: skip-file
"""

Code generated by cian-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client monolith-cian-announcementapi`

cian-codegen version: 1.4.1

"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class HighwayInfo:
    distance: Optional[float] = None
    """Расстояние до города, км"""
    id: Optional[int] = None
    """<a href="http://www.cian.ru/highways.xml" target="_blank">ID шоссе</a>"""
    is_default: Optional[bool] = None
    """Признак основного шоссе (если указано несколько)"""
    name: Optional[str] = None
    """Название"""
