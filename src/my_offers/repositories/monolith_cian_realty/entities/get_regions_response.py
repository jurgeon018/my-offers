# pylint: skip-file
"""

Code generated by cian-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client monolith-cian-realty`

cian-codegen version: 1.4.3

"""
from dataclasses import dataclass
from typing import Optional

from .bounded_by import BoundedBy


@dataclass
class GetRegionsResponse:
    bounded_by: Optional[BoundedBy] = None
    'Bounding-box региона\r\nЕсли у нас в БД у региона нет контуров, то boundedBy будет null'
    display_name: Optional[str] = None
    full_name: Optional[str] = None
    has_districts: Optional[bool] = None
    has_highway: Optional[bool] = None
    has_metro: Optional[bool] = None
    id: Optional[int] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    main_town_id: Optional[int] = None
    name: Optional[str] = None
    time_zone: Optional[int] = None
    """TimeZone региона."""
