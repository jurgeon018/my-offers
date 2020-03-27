from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from my_offers.enums.moderation import ModerationOffenceStatus


@dataclass
class ModerationOfferOffence:
    """Отчетное событиие об изменении данных по видимым нарушениям"""
    offence_id: int
    """ID видимого нарушения"""
    created_date: datetime
    """Дата создания нарушения"""
    created_by: int
    """Кто создал нарушение"""
    object_id: int
    """ID объявления"""
    offence_type: int
    """Тип нарушения"""
    state: ModerationOffenceStatus
    """Статус нарушения"""
    operation_id: str
    """ID операции"""
    date: datetime
    """Дата отправки"""
    text_for_user: str
    """Текст о нарушении для пользователя"""
    row_version: int
    """Версия записи"""
    user_id: Optional[int] = None
    """RealtyUserId объявления"""
    suppose_id: Optional[int] = None
    """ID подозрения"""
    cian_complaint_id: Optional[int] = None
    """ID жалобы"""
    object_region_id: Optional[int] = None
    """Регион объявления"""
    object_category_id: Optional[int] = None
    """Категория объявления"""
    changed_by: Optional[int] = None
    """Кто изменил"""


@dataclass
class OfferOffence:
    offence_id: int
    """ID видимого нарушения"""
    created_date: datetime
    """Дата создания нарушения"""
    created_by: int
    """Кто создал нарушение"""
    offer_id: int
    """ID объявления"""
    offence_type: int
    """Тип нарушения"""
    offence_status: ModerationOffenceStatus
    """Статус нарушения"""
    offence_text: str
    """Текст о нарушении для пользователя"""
    row_version: int
    """Версия записи"""
    created_at: datetime
    """Время создания нарушения"""
    updated_at: datetime
    """Время изменения нарушения"""


@dataclass
class OfferPremoderation:
    offer_id: int
    """Id объявления"""
    removed: bool
    """Санкция снята"""
    row_version: int
    """Версия записи"""
