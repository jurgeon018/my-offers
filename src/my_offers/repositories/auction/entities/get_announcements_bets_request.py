# pylint: skip-file
"""

Code generated by cian-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client auction`

cian-codegen version: 1.9.0

"""
from dataclasses import dataclass
from typing import List


@dataclass
class GetAnnouncementsBetsRequest:
    announcements_ids: List[int]
    """Набор Id объявлений"""
