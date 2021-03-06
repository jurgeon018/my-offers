# pylint: skip-file
"""

Code generated by cian-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client notification-center`

cian-codegen version: 1.4.3

"""
from dataclasses import dataclass
from typing import List

from .mobile_push_settings_child_item_request import MobilePushSettingsChildItemRequest


@dataclass
class MobilePushSettingsParentItemRequest:
    children: List[MobilePushSettingsChildItemRequest]
    """Список настроек мобильных пушей для группы"""
    id: str
    """Идентификатор группы настроек"""
    title: str
    """Название группы настроек мобильных пушей"""
