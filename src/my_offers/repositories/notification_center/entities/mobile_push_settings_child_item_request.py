# pylint: skip-file
"""

Code generated by cian-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client notification-center`

cian-codegen version: 1.4.3

"""
from dataclasses import dataclass


@dataclass
class MobilePushSettingsChildItemRequest:
    description: str
    """Описание настрйоки мобильного пуша"""
    id: str
    """Идентификатор настройки пуша"""
    is_active: bool
    """Флаг вкл/выкл мобильный пуш"""
    title: str
    """Название настройки мобильного пуша"""