from my_offers.repositories.monolith_cian_announcementapi.entities import PublishTerms
from my_offers.repositories.monolith_cian_announcementapi.entities.publish_term import Services
from my_offers.repositories.price_estimator.entities import LiquidityPeriodsRange, LiquidityTermRange


PROMOUTION_SERVICES = [
    Services.premium,
    Services.top3,
    Services.auction,
    Services.highlight
]


def get_liquidity_diapason(
        publish_terms: PublishTerms,
        periods_range: LiquidityPeriodsRange,
) -> str:
    for term in publish_terms.terms:
        for service in term.services:

            if service in PROMOUTION_SERVICES:
                return make_liquidity_str(period=periods_range.period_with_promotion)
    return make_liquidity_str(period=periods_range.regular_period)


def make_liquidity_str(period: LiquidityTermRange) -> str:
    if period.max_selling_term:
        return f'{period.min_selling_term}—{period.max_selling_term}'
    return f'{period.min_selling_term}+'
