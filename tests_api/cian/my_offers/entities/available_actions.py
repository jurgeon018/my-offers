# pylint: skip-file
"""

Code generated by new-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client my-offers`

new-codegen version: 4.0.1

"""
from dataclasses import dataclass


@dataclass
class AvailableActions:
    canMoveToArchive: bool
    """Пользователь может перенести объявление в архив"""
    canUpdateEditDate: bool
    """Можно обновить дату"""
