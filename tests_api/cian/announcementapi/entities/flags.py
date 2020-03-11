# pylint: skip-file
"""

Code generated by new-codegen; DO NOT EDIT.

To re-generate, run `new-codegen generate-client announcementapi`

new-codegen version: 4.0.2

"""
from dataclasses import dataclass
from typing import Optional

from cian_enum import NoFormat, StrEnum


class DraftReason(StrEnum):
    __value_format__ = NoFormat
    calltracking = 'calltracking'
    """Ожидание подмены номера"""
    premoderation = 'premoderation'
    """Премодерация объявления"""
    user = 'user'
    """Отправлено в черновик пользователем"""
    import_ = 'import'
    """Отправлено в черновик импортом"""
    mobile = 'mobile'
    """Отправлено в черновик пользователем через мобильное приложение"""
    moderator = 'moderator'
    """Отправлено в черновик модератором"""
    moderator_from_import = 'moderatorFromImport'
    """Отправлено в черновик модератором через импорт"""
    restore_after_blocked = 'restoreAfterBlocked'
    """Отправлено в черновик после блокировки"""
    fixed_offences = 'fixedOffences'
    """Отправлено в черновик после устранения жалоб"""
    ready_for_package_balancing = 'readyForPackageBalancing'
    """Отправлено в черновик перед балансировкой"""
    ready_for_upload_delete = 'readyForUploadDelete'
    """Отправлено в черновик перед удалением"""
    deferred_publication = 'deferredPublication'
    """Отправлено в черновик перед отложенной публикацией"""
    offences_checked = 'offencesChecked'
    """Проставлен признак "Проверено на ВН\""""


@dataclass
class Flags:
    """Флаги объявления."""

    draftReason: Optional[DraftReason] = None
    """Причина перевода объявления в черновик"""
    isArchived: Optional[bool] = None
    """Объявление архивировано."""
    isDealRent: Optional[bool] = None
    """Объявление из сделки в аренде."""
