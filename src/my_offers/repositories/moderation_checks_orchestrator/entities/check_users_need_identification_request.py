# pylint: skip-file
"""

Code generated by cian-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client moderation-checks-orchestrator`

cian-codegen version: 1.9.0

"""
from dataclasses import dataclass
from typing import List


@dataclass
class CheckUsersNeedIdentificationRequest:
    """Запрос на проверку нужна ли идентификация для этих пользователей"""

    user_ids: List[int]
    """Ids пользователей"""
