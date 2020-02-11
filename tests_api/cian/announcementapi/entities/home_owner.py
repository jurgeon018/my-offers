# pylint: skip-file
"""

Code generated by new-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client announcementapi`

new-codegen version: 4.0.0

"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class HomeOwner:
    """Информация о собственнике"""

    cadastralNumber: Optional[str] = None
    """Кадастровый номер"""
    firstName: Optional[str] = None
    """Имя собственника"""
    flatNumber: Optional[str] = None
    """Номер квартиры"""
    houseNumber: Optional[str] = None
    """Номер дома"""
    lastName: Optional[str] = None
    """Фамилия собственника"""
    secondName: Optional[str] = None
    """Отчетство собственника"""
