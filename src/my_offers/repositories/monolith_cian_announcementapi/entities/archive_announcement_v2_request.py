# pylint: skip-file
"""

Code generated by cian-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client monolith-cian-announcementapi`

cian-codegen version: 1.5.0

"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class ArchiveAnnouncementV2Request:
    """Запрос на архивацию объявления"""

    announcement_id: Optional[int] = None
    """Id Объявления"""
