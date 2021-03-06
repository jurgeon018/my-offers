# pylint: skip-file
"""

Code generated by cian-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client monolith-cian-ms-announcements`

cian-codegen version: 1.9.0

"""
from dataclasses import dataclass
from typing import Optional

from cian_enum import NoFormat, StrEnum


class Status(StrEnum):
    __value_format__ = NoFormat
    draft = 'Draft'
    """11 - Черновик"""
    published = 'Published'
    """12 - Опубликовано"""
    deactivated = 'Deactivated'
    """14 - Деактивировано (ранее было скрыто Hidden)"""
    refused = 'Refused'
    """15 - Отклонено модератором"""
    deleted = 'Deleted'
    """16 - Удалён"""
    sold = 'Sold'
    """17 - Продано/Сдано"""
    moderate = 'Moderate'
    '18 - Требует модерации\r\nДанный статус исчез - оставим для совместимости'
    removed_by_moderator = 'RemovedByModerator'
    """19 - Удалено модератором"""
    blocked = 'Blocked'
    """20 - объявление снято с публикации по причине применения санкции "приостановки публикации\""""


@dataclass
class ChangedAnnouncement:
    """Изменившиеся объявление"""

    id: int
    """Id объявления"""
    flags: Optional[int] = None
    """Флаги объявления"""
    row_version: Optional[int] = None
    """RowVersion"""
    status: Optional[Status] = None
    """Статус объявления"""
