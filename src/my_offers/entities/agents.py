from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from my_offers.enums.agents import AgentAccountType


@dataclass
class Phone:
    id: int
    """ID телефона"""
    number: str
    """Номер"""
    confirmed: bool
    """Подтвержден"""
    visible: bool
    """Виден"""
    country_code: Optional[str] = None
    """Код страны"""
    code: Optional[str] = None
    """Код города"""


@dataclass
class AgentMessage:
    id: int
    """ID агента"""
    row_version: int
    """Версия записи"""
    realty_user_id: Optional[int] = None
    """ID пользователя"""
    master_agent_user_id: Optional[int] = None
    """ID пользователя мастера-агента"""
    account_type: Optional[AgentAccountType] = None
    """Тип агента"""
    middle_name: Optional[str] = None
    """Отчетсво"""
    first_name: Optional[str] = None
    """Имя"""
    last_name: Optional[str] = None
    """Фамилия"""
    agency_name: Optional[str] = None
    """Название компании"""
    skype: Optional[str] = None
    """skype"""
    contact_email: Optional[str] = None
    """Контактная почта"""
    website: Optional[str] = None
    """Ссылка на сайт"""
    birth_date: Optional[datetime] = None
    """День рождния"""
    experience: Optional[str] = None
    """Опыт работы"""
    description: Optional[str] = None
    """Описание"""
    office_name: Optional[str] = None
    """Название офиса"""
    phones: Optional[List[str]] = None
    """Телефоны"""
    phones_data: Optional[List[Phone]] = None
    """Инофрмация о телефонах"""
    creation_date: Optional[datetime] = None
    """Дата создания агента"""
    name: Optional[str] = None
    """Полное имя"""
    operation_id: Optional[str] = None
    """ID операции"""
    date: Optional[datetime] = None
    """Время отправки"""


@dataclass
class Agent:
    id: int
    """ID агента"""
    row_version: int
    """Версия записи"""
    created_at: datetime
    """Время создания"""
    updated_at: datetime
    """Время изменения"""
    realty_user_id: Optional[int] = None
    """ID пользователя"""
    master_agent_user_id: Optional[int] = None
    """ID пользователя мастераагента"""
    account_type: Optional[AgentAccountType] = None
    """Тип агента"""
    middle_name: Optional[str] = None
    """Отчетсво"""
    first_name: Optional[str] = None
    """Имя"""
    last_name: Optional[str] = None
    """Фамилия"""


@dataclass
class AgentName:
    id: int
    """ID пользователя"""
    middle_name: Optional[str]
    """Отчетсво"""
    first_name: Optional[str]
    """Имя"""
    last_name: Optional[str]
    """Фамилия"""

    def get_name(self) -> Optional[str]:
        result = []
        if self.first_name:
            result.append(self.first_name)

        if self.last_name:
            result.append(self.last_name)

        if not result:
            return None

        return ' '.join(result)


@dataclass
class AgentHierarchyData:
    is_master_agent: bool
    """Является ли пользователь мастер-агентом"""
    is_sub_agent: bool
    """Является ли пользователь саб-агентом"""

    @property
    def is_agent(self) -> bool:
        """Является ли пользователь агентом без иерархии"""
        return not any([self.is_master_agent, self.is_sub_agent])
