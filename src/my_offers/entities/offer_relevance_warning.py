from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class OfferRelevanceWarning:
    offer_id: int
    """ID объявления"""
    check_id: str
    """ID проверки"""
    created_at: datetime
    """Дата создания"""
    updated_at: datetime
    """Дата последнего обновления"""
    due_date: Optional[datetime] = None
    """Дата автоматического снятия объявления с публикации"""
    active: Optional[bool] = None
    """Проверка не завершена"""
