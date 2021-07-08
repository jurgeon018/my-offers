# pylint: skip-file
"""

Code generated by cian-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client agents`

cian-codegen version: 1.15.1

"""
from dataclasses import dataclass
from typing import List

from .agent_response import AgentResponse


@dataclass
class AgentsListResponse:
    """Модель списка сотрудников."""

    agents: List[AgentResponse]
    """Сотрудники"""
    page: int
    """Номер страницы"""
    page_size: int
    """Размер страницы"""
    pages_count: int
    """Количество страниц"""
    total_count: int
    """Общее количество сабегетов"""
