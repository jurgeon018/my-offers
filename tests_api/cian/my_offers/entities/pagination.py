# pylint: skip-file
"""

Code generated by new-codegen; DO NOT EDIT.

To re-generate, run `new-codegen generate-client my-offers`

new-codegen version: 4.0.2

"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Pagination:
    limit: Optional[int] = None
    """Количество объявлений на страницу"""
    offset: Optional[int] = None
    """Отступ от начала"""
    page: Optional[int] = None
    """Номер страницы начиная с 1"""
