from dataclasses import dataclass
from typing import List

from my_offers import enums


@dataclass
class GetOfferValuationRequest:
    offer_id: int
    """Id объявления"""


@dataclass
class ValuationOption:
    value: str
    """Значение"""
    description: str
    """Описание"""


@dataclass
class InfoRelativeMarket:
    price_estimate: enums.PriceEstimate
    """оценка цены"""
    title: str
    """Заголовок"""
    text: str
    """Текст"""
    hint: str
    """Подсказка"""


@dataclass
class GetOfferValuationResponse:
    valuation_options: List[ValuationOption]
    """Информация оценки"""
    info_relative_market: InfoRelativeMarket
    """Информация относительно рынка"""
    valuation_block_link_share: str
    """Ссылка для кнопки поделиться"""
    valuation_block_link_report: str
    """Ссылка на отчет"""
