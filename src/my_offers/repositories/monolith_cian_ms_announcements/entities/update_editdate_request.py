# pylint: skip-file
"""

Code generated by cian-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client monolith-cian-ms-announcements`

cian-codegen version: 1.4.1

"""
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class UpdateEditdateRequest:
    """Запрос на обновление даты публикации для списка объявлений."""

    ids: Optional[List[int]] = None
    """Список id объявлений для обновления даты публикации."""
