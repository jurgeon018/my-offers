# pylint: skip-file
"""

Code generated by cian-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client moderation`

cian-codegen version: 1.9.0

"""
from dataclasses import dataclass
from typing import List


@dataclass
class GetVideoOffencesForAnnouncementsRequest:
    """Запрос на получение нарушений для скрытых видео"""

    announcement_ids: List[int]
    """Идентификаторы объявлений"""
