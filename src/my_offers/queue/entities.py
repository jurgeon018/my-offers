from dataclasses import dataclass
from datetime import datetime
from typing import Dict

from my_offers import entities


@dataclass
class AnnouncementMessage:
    model: Dict
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
