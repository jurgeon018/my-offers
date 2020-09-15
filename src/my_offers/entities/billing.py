from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from my_offers import enums


@dataclass
class AnnouncementBillingContract:
    id: int
    """Id записи в БД announcementapi"""
    user_id: int
    """Id пользователя - владельца контракта (и соответственно объявления)"""
    actor_user_id: int
    """Id пользователя - инициатора применения услуги"""
    publisher_user_id: int
    """Id пользователя (того за чей счет публикация т.е. publisherAccountId в таблице контрактов)"""
    start_date: datetime
    """Дата начала действия"""
    payed_till: datetime
    """Дата, до которой оплачен контракт"""
    target_object_id: int
    """Id объекта применения"""
    target_object_type: enums.TargetObjectType
    """Тип объекта"""
    service_types: List[enums.OfferServiceTypes]
    """Услуги"""
    service_package_group_id: Optional[int] = None
    """Id группы слотов в пакете. Заполняется при размещении объявления из пакета"""
    closed_date: Optional[datetime] = None
    """Дата закрытия контракта"""
    row_version: Optional[int] = None
    """Версия записи"""


@dataclass
class OfferBillingContract:
    id: int
    """ID контракта"""
    user_id: int
    """Id пользователя - владельца контракта (и соответственно объявления)"""
    actor_user_id: int
    """Id пользователя - инициатора применения услуги"""
    publisher_user_id: int
    """Id пользователя (того за чей счет публикация т.е. publisherAccountId в таблице контрактов)"""
    start_date: datetime
    """Дата начала действия"""
    payed_till: datetime
    """Дата, до которой оплачен контракт"""
    offer_id: int
    """ID объявления"""
    row_version: Optional[int]
    """Версия записи"""
    is_deleted: bool
    """Макер удален ли контракт"""
    created_at: datetime
    """Время создания контракта"""
    updated_at: datetime
    """Время изменения контракта"""
    service_types: List[enums.OfferServiceTypes]
    """Услуги"""
