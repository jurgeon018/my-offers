from typing import List

from my_offers.entities import ValuationOption
from my_offers.enums import DealType
from my_offers.repositories.monolith_cian_announcementapi.entities import PublishTerms
from my_offers.repositories.price_estimator.entities import GetEstimationForRealtorsResponse
from my_offers.services.valuation.fields.liquidity import get_liquidity_range
from my_offers.services.valuation.helpers.pretty_price import get_pretty_market_price, get_pretty_price_range


def get_valuation_options(
        *,
        deal_type: DealType,
        publish_terms: PublishTerms,
        valuation_response: GetEstimationForRealtorsResponse
) -> List[ValuationOption]:
    market_price_str = get_pretty_market_price(price=valuation_response.prices.price)
    price_diapason = get_pretty_price_range(
        price_min=valuation_response.prices.price_min,
        price_max=valuation_response.prices.price_max,
    )
    if deal_type.is_rent:
        return [
            ValuationOption(
                value=f'{market_price_str}\xa0₽/мес',
                description='Рыночная\xa0ставка'
            ),
            ValuationOption(
                value=f'{price_diapason}\xa0₽/мес',
                description='Диапазон\xa0ставки'
            ),
        ]

    liquidity_diapason = get_liquidity_range(
        publish_terms=publish_terms,
        periods_range=valuation_response.liquidity_periods,
    )
    return [
        ValuationOption(
            value=f'{market_price_str}\xa0₽',
            description='Рыночная\xa0цена\xa0этой\xa0квартиры'
        ),
        ValuationOption(
            value=f'{price_diapason}\xa0₽',
            description='Диапазон\xa0цены'
        ),
        ValuationOption(
            value=f'{liquidity_diapason}\xa0дней',
            description='Прогнозируемый срок продажи при текущей цене квартиры и продвижении'
        )
    ]
