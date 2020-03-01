from dataclasses import dataclass
from datetime import datetime

from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel

from my_offers import entities


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
    service_contract_reporting_model: entities.OfferBillingContract
    """Cобытие изменения контрактов"""
    operation_id: str
    """Operation id"""
    date: datetime
    """Время изменения"""
