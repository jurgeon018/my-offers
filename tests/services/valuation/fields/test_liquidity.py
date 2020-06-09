import pytest

from my_offers.repositories.monolith_cian_announcementapi.entities import PublishTerm, PublishTerms
from my_offers.repositories.monolith_cian_announcementapi.entities.publish_term import Services
from my_offers.repositories.price_estimator.entities import LiquidityPeriodsRange, LiquidityTermRange
from my_offers.services.valuation.fields.liquidity import get_liquidity_diapason


@pytest.mark.parametrize(
    ('publish_terms', 'periods_range', 'expected'),
    (
        (
            PublishTerms(terms=[PublishTerm(services=[Services.top3])]),
            LiquidityPeriodsRange(
                regular_period=LiquidityTermRange(min_selling_term=50, max_selling_term=60),
                period_with_promotion=LiquidityTermRange(min_selling_term=20, max_selling_term=30)
            ),
            '20—30'
        ),
        (
            PublishTerms(terms=[PublishTerm(services=[Services.paid, Services.auction])]),
            LiquidityPeriodsRange(
                regular_period=LiquidityTermRange(min_selling_term=120, max_selling_term=None),
                period_with_promotion=LiquidityTermRange(min_selling_term=120, max_selling_term=None)
            ),
            '120+'
        ),
        (
            PublishTerms(terms=[PublishTerm(services=[Services.free])]),
            LiquidityPeriodsRange(
                regular_period=LiquidityTermRange(min_selling_term=50, max_selling_term=60),
                period_with_promotion=LiquidityTermRange(min_selling_term=20, max_selling_term=30)
            ),
            '50—60'
        ),
        (
            PublishTerms(terms=[PublishTerm(services=[Services.paid])]),
            LiquidityPeriodsRange(
                regular_period=LiquidityTermRange(min_selling_term=120, max_selling_term=None),
                period_with_promotion=LiquidityTermRange(min_selling_term=90, max_selling_term=120)
            ),
            '120+'
        ),
    )
)
def test_get_liquidity_diapason(mocker, publish_terms, periods_range, expected):
    # arrange & act
    result = get_liquidity_diapason(
        publish_terms=publish_terms,
        periods_range=periods_range,
    )

    # assert
    assert result == expected
