# pylint: skip-file
"""

Code generated by new-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client qa-cian-proxy`

new-codegen version: 4.0.0

"""
from dataclasses import dataclass

from .new_user_response import NewUserResponse


@dataclass
class QaNewUserCrested:
    createdUser: NewUserResponse
    """Созданный qa user"""
    isPrepared: bool
    """Флаг: создан ли пользователь или взят из базы"""
    phone: str
    """Телефон"""