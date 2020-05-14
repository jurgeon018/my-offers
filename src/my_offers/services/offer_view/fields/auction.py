from typing import Optional

from my_offers.repositories.monolith_cian_announcementapi.entities.bargain_terms import Currency
from my_offers.services.offer_view.constants import CURRENCY


def get_auction_bet(bet: Optional[float]) -> Optional[str]:
    if not bet:
        return None

    return '+{}\xa0{}'.format(int(bet), CURRENCY[Currency.rur])
