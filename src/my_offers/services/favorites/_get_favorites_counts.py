from typing import Dict, List

from cian_core.degradation import get_degradation_handler

from my_offers.repositories.favorites import v1_get_offers_favorites_count
from my_offers.repositories.favorites.entities import OfferFavoriteCount


async def get_favorites_counts(offer_ids: List[int]) -> Dict[int, int]:
    response: List[OfferFavoriteCount] = await v1_get_offers_favorites_count(offer_ids)

    return {item.offer_id: item.count for item in response}


get_favorites_counts_degradation_handler = get_degradation_handler(
    func=get_favorites_counts,
    key='cassandra.get_favorites_counts',
    default=dict(),
)
