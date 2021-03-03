# pylint: skip-file
"""

Code generated by cian-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client monolith-cian-announcementapi`

cian-codegen version: 1.9.0

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

    draft_reason: Optional[DraftReason] = None
    """Причина перевода объявления в черновик"""
    is_archived: Optional[bool] = None
    """Объявление архивировано."""
    is_commercial_ownership_verified: Optional[bool] = None
    """Объявление от собственника коммерческой с проверенным правом собственности."""
    is_deal_rent: Optional[bool] = None
    """Объявление из сделки в аренде."""
