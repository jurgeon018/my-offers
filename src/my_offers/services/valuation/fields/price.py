from typing import Optional

from cian_web.exceptions import BrokenRulesException, Error

from my_offers.repositories.monolith_cian_announcementapi.entities.bargain_terms import Currency


USD_RUR = 70
EUR_RUR = 80

# todo https://jira.cian.tech/browse/CD-82073


def get_price_rur(
        *,
        price: Optional[float],
        currency: Currency,
) -> int:
    if not price:
        raise BrokenRulesException([
            Error(
                message='offer object_model has uncorrect price '
                        'valuation can not be provided without price',
                code='valuation_not_poossible',
                key='price'
            )
        ])
    if currency == Currency.usd:
        return int(price * USD_RUR)
    if currency == Currency.eur:
        return int(price * EUR_RUR)
    return int(price)
