# pylint: skip-file
"""

Code generated by new-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client my-offers`

new-codegen version: 4.0.1

"""
from dataclasses import dataclass


@dataclass
class Underground:
    lineColor: str
    """Цвет линии метро"""
    name: str
    """Название метро"""
    regionId: int
    """ID региона"""
    searchUrl: str
    """Поисковый запрос по метро"""
