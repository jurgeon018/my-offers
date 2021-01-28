# pylint: skip-file
"""

Code generated by cian-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client monolith-cian-ms-announcements`

cian-codegen version: 1.9.0

"""
from dataclasses import dataclass
from typing import List

from .changed_announcement import ChangedAnnouncement


@dataclass
class GetChangedIdsV2Response:
    """Ответ на запрос получения изменившихся объявлений"""

    announcements: List[ChangedAnnouncement]
    """Объявления"""
