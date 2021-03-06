# pylint: skip-file
"""

Code generated by cian-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client agents`

cian-codegen version: 1.15.1

"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class AgentServicePackagesLimits:
    """Данные по пакетам объявлений пользователя"""

    highlight_count: Optional[int] = None
    """Количество задействованных слотов в категории Выделение цветом"""
    highlight_limit: Optional[int] = None
    """Лимит объявлений в категории Выделение цветом"""
    paid_count: Optional[int] = None
    """Количество задействованных слотов в категории Платное"""
    paid_limit: Optional[int] = None
    """Лимит объявлений в категории Платное"""
    premium_count: Optional[int] = None
    """Количество задействованных слотов в категории Премиум"""
    premium_limit: Optional[int] = None
    """Лимит объявлений в категории Премиум"""
    top3_count: Optional[int] = None
    """Количество задействованных слотов в категории ТОП3"""
    top3_limit: Optional[int] = None
    """Лимит объявлений в категории ТОП3"""
