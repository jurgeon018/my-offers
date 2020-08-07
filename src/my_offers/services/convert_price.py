import math
from typing import Dict

from cian_cache import CachedOptions, cached
from simple_settings import settings

from my_offers.repositories.monolith_cian_announcementapi.entities.bargain_terms import Currency
from my_offers.repositories.monolith_cian_realty import api_currencies


async def get_price_rur(
        *,
        price: float,
        currency: Currency,
) -> int:
    if currency.is_rur:
        return math.ceil(price)

    currencies = await _get_currencies()

    return math.ceil(price * currencies[currency.value.lower()])


@cached(
    group='currencies-v3',
    options=CachedOptions(ttl=settings.CURRENCIES_TTL),
)
async def _get_currencies() -> Dict[Currency, float]:
    """Получение курсов валют из монолита шарпа"""
    currencies = await api_currencies()
    result = {
        currency.currency_code.lower(): currency.rate
        for currency in currencies
    }

    return result
