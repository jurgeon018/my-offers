from typing import List

from my_offers.entities import ValuationOption
from my_offers.enums import DealType
from my_offers.repositories.monolith_cian_announcementapi.entities import PublishTerms
from my_offers.repositories.price_estimator.entities import GetEstimationForRealtorsResponse
from my_offers.services.valuation.fields.liquidity import get_liquidity_range
from my_offers.services.valuation.helpers.pretty_price import get_pretty_market_price, get_pretty_price_range


OPTION_DESCRIPTION = {
    'market_price': {
        DealType.rent: 'Рыночная\xa0ставка',
        DealType.sale: 'Рыночная\xa0цена\xa0этой\xa0квартиры',
    },
    'price_range': {
        DealType.rent: 'Диапазон\xa0ставки',
        DealType.sale: 'Диапазон\xa0цены',
    },
}


def get_valuation_options(
        *,
        deal_type: DealType,
        publish_terms: PublishTerms,
        valuation_response: GetEstimationForRealtorsResponse
) -> List[ValuationOption]:
    market_price = get_pretty_market_price(price=valuation_response.prices.price)
    market_price_str = market_price + '\xa0₽' + ('/мес' if deal_type.is_rent else '')

    price_range = get_pretty_price_range(
        price_min=valuation_response.prices.price_min,
        price_max=valuation_response.prices.price_max,
    )
    price_range_str = price_range + '\xa0₽' + ('/мес' if deal_type.is_rent else '')

    result = [
        ValuationOption(
            value=market_price_str,
            description=OPTION_DESCRIPTION['market_price'][deal_type]
        ),
        ValuationOption(
            value=price_range_str,
            description=OPTION_DESCRIPTION['price_range'][deal_type]
        ),
    ]

    if deal_type.is_sale and valuation_response.liquidity_periods:

        liquidity_diapason = get_liquidity_range(
            publish_terms=publish_terms,
            periods_range=valuation_response.liquidity_periods,
        )
        result.append(
            ValuationOption(
                value=f'{liquidity_diapason}\xa0дней',
                description='Прогнозируемый срок продажи при текущей цене квартиры и продвижении'
            )
        )

    return result
