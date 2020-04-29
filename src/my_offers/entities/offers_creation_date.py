from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class OffersCreationDateRequest:
    master_user_id: int
    """Id мастер агента"""
    offer_ids: List[int]
    """Список id объявлений"""


@dataclass
class OfferCreationDate:
    offer_id: int
    """id объявления"""
    creation_date: Optional[datetime]
    """дата создания"""


@dataclass
class OffersCreationDateResponse:
    offers: List[OfferCreationDate]
    """Список объявлений"""


@dataclass
class OfferRowVersion:
    offer_id: int
    """id объявления"""
    row_version: int
    """Версия записи"""
