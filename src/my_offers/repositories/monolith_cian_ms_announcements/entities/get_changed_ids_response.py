# pylint: skip-file
"""

Code generated by cian-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client monolith-cian-ms-announcements`

cian-codegen version: 1.4.1

"""
from dataclasses import dataclass
from typing import List


@dataclass
class GetChangedIdsResponse:
    """Ответ на запрос на получение изменившихся объявлений"""

    offers_ids: List[int]
    """Ids объявлений"""
