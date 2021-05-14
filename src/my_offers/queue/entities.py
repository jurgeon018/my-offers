from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from my_offers import entities
from my_offers.enums.notifications import UserNotificationType
from my_offers.queue import enums
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
    object_id: int
    """Id объявления"""
    operation_id: str
    """Operation id"""
    date: datetime
    """Время изменения"""
    row_version: int
    """Версия записи"""


@dataclass
class NeedUpdateDuplicateMessage:
    id: int
    """Id объявления"""
    force: bool
    """Принудительное обновление"""
    date: datetime
    """Время изменения"""


@dataclass
class OfferNewDuplicateMessage:
    duplicate_offer_id: int
    """Id объявления дубликата"""
    operation_id: str
    """Operation id"""
    date: datetime
    """Время изменения"""


@dataclass
class OfferDuplicatePriceChangedMessage:
    duplicate_offer_id: int
    """Id объявления дубликата"""
    operation_id: str
    """Operation id"""
    date: datetime
    """Время изменения"""


@dataclass
class OfferDuplicateEvent:
    user_id: int
    """realtyUserId пользователя"""
    event_type: enums.PushType
    """Тип события"""
    object_id: int
    """id объявки риэлтора"""
    similar_object_id: int
    """id объявки-дубля"""
    similar_object_price: Optional[int]
    """цена объявки-дубля в рублях"""
    region_id: Optional[int]
    """id региона, в котором публикуется объявление-дубль или меняется цена на него"""
    operation_id: str
    """идентификатор операции"""
    transport: UserNotificationType
    """Тип пуша"""


@dataclass
class DeleteUserDataMessage:
    operation_id: str
    """идентификатор операции"""
    user_id: int
    """Id пользователя"""


@dataclass
class OfferRelevanceWarningMessage:
    realty_object_id: int
    """Id объявления"""
    check_status_id: str
    """Статус"""
    guid: str
    """Идентификатор проверки"""
    date: datetime
    """Время изменения"""
    decline_date: Optional[datetime] = None
    """Планируемая дата отклонения объявления"""
    relevance_type_message: Optional[str] = None
    """Тип сообщения для пользователя"""


@dataclass
class UpdateOfferMasterUserMessage:
    offer_id: int
    """Идентификатор объявления"""
    new_master_user_id: int
    """Идентификатор нового мастера объявления"""
    operation_id: str
    """Operation id"""
    date: datetime
    """Время изменения"""
