# pylint: skip-file
"""

Code generated by cian-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client monolith-cian-bill`

cian-codegen version: 1.15.0

"""
from dataclasses import dataclass
from typing import List


@dataclass
class V1TarifficationGetDeactivatedAdditionalServices:
    announcement_ids: List[int]
    """ID объявлений."""
    user_id: int
    """Realty Id пользователя."""
