# pylint: skip-file
"""

Code generated by new-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client qa-cian-proxy`

new-codegen version: 4.0.0

"""
from dataclasses import dataclass
from typing import Optional

from .new_user_request import NewUserRequest


@dataclass
class QaNewUser:
    user: NewUserRequest
    """Параметры qa user"""
    createNew: Optional[bool] = None
    """Флаг: создвать ли нового пользователя"""
