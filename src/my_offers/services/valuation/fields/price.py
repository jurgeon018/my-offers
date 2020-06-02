from my_offers.repositories.monolith_cian_announcementapi.entities.bargain_terms import Currency


USD_RUR = 70
EUR_RUR = 80

# https://jira.cian.tech/browse/CD-82073


def get_price_rur(
        price: float,
        currency: Currency,
) -> int:
    if currency == Currency.usd:
        return int(price * USD_RUR)
    if currency == Currency.eur:
        return int(price * EUR_RUR)
    return int(price)
