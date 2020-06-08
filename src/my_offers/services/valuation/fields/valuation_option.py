from typing import List

from my_offers.entities import ValuationOption
from my_offers.enums import DealType
from my_offers.repositories.price_estimator.entities import GetEstimationForRealtorsResponse


# todo https://jira.cian.tech/browse/CD-82139 нормальное форматирование респонса


def get_valuation_options(
        deal_type: DealType,
        valuation_response: GetEstimationForRealtorsResponse
) -> List[ValuationOption]:
    result = [
        ValuationOption(
            value=f'{valuation_response.prices.price}\xa0₽/мес',
            description='Рыночная\xa0ставка'
        ),
        ValuationOption(
            value=f'{valuation_response.prices.price_min}—{valuation_response.prices.price_max}\xa0₽/мес',
            description='Диапазон\xa0ставки'
        ),
    ]
    if deal_type == DealType.sale:
        result.append(
            ValuationOption(
                value=f'{valuation_response.liquidity_periods.period_with_promotion.min_selling_term}—'
                      f'{valuation_response.liquidity_periods.period_with_promotion.max_selling_term} дней',
                description='Прогнозируемый срок продажи при текущей цене квартиры и продвижении'
            )
        )
    return result
