# pylint: skip-file
"""

Code generated by cian-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client users`

cian-codegen version: 1.7.1

"""
from dataclasses import dataclass
from typing import List

from .user_model import UserModel


@dataclass
class GetUsersResponse:
    """Список  моделей пользователей"""

    users: List[UserModel]
    """Модели пользователей"""
