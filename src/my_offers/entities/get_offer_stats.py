from dataclasses import dataclass
from datetime import date
from typing import List, Optional, Type

from my_offers import enums


@dataclass
class GetOfferStatsV1Request:
    offer_id: int
    """Id объявления"""
    deal_type: enums.DealType
    """Тип сделки"""
    offer_type: enums.OfferType
    """Тип объекта недвижимости"""


@dataclass
class ChartData:
    date: date
    """Дата"""
    value: int
    """Значание"""


@dataclass
class PeriodStats:
    coverage: Optional[float] = None
    """Охват аудитории"""
    favorites: Optional[int] = None
    """Количество добавлений в избранное"""
    offer_show: Optional[int] = None
    """Просмотров объявления за период"""
    offer_show_total: Optional[int] = None
    """Просмотров объявления за все время"""
    phone_show: Optional[int] = None
    """Просмотров телефона"""
    calls_total: Optional[int] = None
    """Количество звонков за все время"""
    search_results_selected_chart: Optional[List[ChartData]] = None
    """График: Поиски, под которые подошел ваш объект"""
    search_results_show_chart: Optional[List[ChartData]] = None
    """График: Увидели ваш объект в поиске"""
    show_chart: Optional[List[ChartData]] = None
    """График: Просмотры объявления"""


@dataclass
class StatsData:
    day10: PeriodStats
    """Статистика за 10 дней"""
    month: PeriodStats
    """Статистика за месяц"""


@dataclass
class EmergencyMessage:
    text: str
    """Текст"""


@dataclass
class GetOfferStatsV1Response:
    data: StatsData
    """Данные статистики"""
    emergency_message: Optional[EmergencyMessage] = None
    """Экстренное сообщение о разделе Статистика"""
