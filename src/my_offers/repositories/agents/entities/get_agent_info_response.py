# pylint: skip-file
"""

Code generated by cian-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client agents`

cian-codegen version: 1.15.1

"""
from dataclasses import dataclass
from typing import Optional

from cian_enum import NoFormat, StrEnum


class AgentType(StrEnum):
    __value_format__ = NoFormat
    agent = 'agent'
    """Агент"""
    agency = 'agency'
    """Агентство"""
    sub_agent = 'subAgent'
    """Сабагент"""


@dataclass
class GetAgentInfoResponse:
    """Модель для получения информации об агенте"""

    agent_id: int
    """Id агента"""
    agent_type: AgentType
    """Тип агента"""
    user_id: int
    """UserId агента"""
    agency_name: Optional[str] = None
    """Название агентства"""
    cian_user_id: Optional[int] = None
    """CianUserId"""
    company_id: Optional[int] = None
    """Id компании"""
    contact_email: Optional[str] = None
    """Почта для контактов"""
    first_name: Optional[str] = None
    """Имя агента"""
    last_name: Optional[str] = None
    """Фамилия агента"""
    master_agent_id: Optional[int] = None
    """AgentId мастер агента (существует только у сабагентов)"""
    master_user_id: Optional[int] = None
    """RealtyUserId мастер агента (существует только у сабагентов)"""
    name: Optional[str] = None
    """Для агента пишется ФИО, для агентства - название агентства"""
    website: Optional[str] = None
    """Сайт агентства"""