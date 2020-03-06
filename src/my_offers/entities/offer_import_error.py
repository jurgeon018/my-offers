from dataclasses import dataclass
from datetime import datetime


@dataclass
class OfferImportError:
    offer_id: int
    """Id объявления"""
    type: str
    """Тип ошибки"""
    message: str
    """Сообщение об ошибки"""
    created_at: datetime
    """Дата создания"""
