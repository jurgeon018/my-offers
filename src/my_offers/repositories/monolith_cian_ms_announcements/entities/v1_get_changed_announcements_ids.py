# pylint: skip-file
"""

Code generated by cian-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client monolith-cian-ms-announcements`

cian-codegen version: 1.4.1

"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class V1GetChangedAnnouncementsIds:
    row_version: int
    """RowVersion объявления"""
    top: Optional[int] = None
    """Количество"""
