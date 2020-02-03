# pylint: skip-file
"""

Code generated by cian-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client monolith-cian-announcementapi`

cian-codegen version: 1.4.1

"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class RentByParts:
    """Класс для представления части помещения в аренду"""

    area: Optional[float] = None
    """Площадь части"""
    price: Optional[float] = None
    """Стоимость части"""
