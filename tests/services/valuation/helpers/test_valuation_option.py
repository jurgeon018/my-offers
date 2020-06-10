import pytest

from my_offers.entities import ValuationOption
from my_offers.enums import DealType
from my_offers.repositories.monolith_cian_announcementapi.entities import PublishTerm, PublishTerms
from my_offers.repositories.monolith_cian_announcementapi.entities.publish_term import Services
from my_offers.repositories.price_estimator.entities import (
    GetEstimationForRealtorsResponse,
    LiquidityPeriodsRange,
    LiquidityTermRange,
    PriceWithRange,
)
from my_offers.services.valuation.helpers.valuation_option import get_valuation_options


@pytest.mark.parametrize(
    ('deal_type', 'publish_terms', 'valuation_response', 'expected'),
    (
        (
            DealType.rent,
            PublishTerms(terms=[PublishTerm(services=[Services.paid])]),
            GetEstimationForRealtorsResponse(
                liquidity_periods=LiquidityPeriodsRange(
                    regular_period=LiquidityTermRange(min_selling_term=50, max_selling_term=60),
                    period_with_promotion=LiquidityTermRange(min_selling_term=20, max_selling_term=30)
                ),
                prices=PriceWithRange(
                    price=30_000,
                    price_min=25_000,
                    price_max=35_000,
                ),
                url='http://www.master.dev3.cian.ru/kalkulator-nedvizhimosti/'
            ),
            [
                ValuationOption(
                    value='30\xa0000\xa0₽/мес',
                    description='Рыночная\xa0ставка'
                ),
                ValuationOption(
                    value='25\xa0000—35\xa0000\xa0₽/мес',
                    description='Диапазон\xa0ставки'
                ),
            ]
        ),
        (
            DealType.sale,
            PublishTerms(terms=[PublishTerm(services=[Services.premium, Services.auction])]),
            GetEstimationForRealtorsResponse(
                liquidity_periods=LiquidityPeriodsRange(
                    regular_period=LiquidityTermRange(min_selling_term=50, max_selling_term=60),
                    period_with_promotion=LiquidityTermRange(min_selling_term=20, max_selling_term=30)
                ),
                prices=PriceWithRange(
                    price=10_000_000,
                    price_min=9_900_000,
                    price_max=10_100_000,
                ),
                url='http://www.master.dev3.cian.ru/kalkulator-nedvizhimosti/'
            ),
            [
                ValuationOption(
                    value='10 млн\xa0₽',
                    description='Рыночная\xa0цена\xa0этой\xa0квартиры'
                ),
                ValuationOption(
                    value='9,9—10,1\xa0млн\xa0₽',
                    description='Диапазон\xa0цены'
                ),
                ValuationOption(
                    value='20—30\xa0дней',
                    description='Прогнозируемый срок продажи при текущей цене квартиры и продвижении'
                )
            ]
        ),


    )
)
def test_get_valuation_options(mocker, deal_type, publish_terms, valuation_response, expected):
    # arrange & act
    result = get_valuation_options(
        deal_type=deal_type,
        publish_terms=publish_terms,
        valuation_response=valuation_response
    )

    # assert
    assert result == expected
