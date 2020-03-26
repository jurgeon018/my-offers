from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from my_offers import entities
from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel


@dataclass
class AnnouncementMessage:
    model: ObjectModel
    """Объявление"""
    operation_id: str
    """Operation id"""
    date: datetime
    """Время изменения"""


@dataclass
class ServiceContractMessage:
    service_contract_reporting_model: entities.AnnouncementBillingContract
    """Cобытие изменения контрактов"""
    operation_id: str
    """Operation id"""
    date: datetime
    """Время изменения"""


@dataclass
class SaveUnloadError:
    type: str
    """Тип ошибки"""
    message: str
    """Сообщение об ошибки"""


@dataclass
class SaveUnloadErrorMessage:
    object_id: Optional[int]
    """Id объявления"""
    operation_id: str
    """Operation id"""
    date: datetime
    """Время изменения"""
    error: SaveUnloadError
    """Произошедшая ошибка"""


@dataclass
class AnnouncementPremoderationReportingMessage:
    object_id: Optional[int]
    """Id объявления"""
    operation_id: str
    """Operation id"""
    date: datetime
    """Время изменения"""
    row_version: Optional[int] = None
    """Версия записи"""
