from dataclasses import dataclass
from datetime import datetime
from typing import Dict


@dataclass
class AnnouncementMessage:
    model: Dict
    """Объявление"""
    operation_id: str
    """Operation id"""
    date: datetime
    """Время изменения"""
