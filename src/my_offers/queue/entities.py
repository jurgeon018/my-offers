from dataclasses import dataclass
from datetime import datetime

from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel


@dataclass
class AnnouncementMessage:
    model: ObjectModel
    """Объявление"""
    operation_id: str
    """Operation id"""
    date: datetime
    """Время изменения"""
