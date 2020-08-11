from typing import Dict, List

from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel
from my_offers.repositories.monolith_cian_announcementapi.entities.publish_term import Services
from my_offers.services.auctions import get_auction_bets_degradation_handler


async def load_auction_bets(object_models: List[ObjectModel]) -> Dict[int, int]:
    offer_ids = []
    for object_model in object_models:
        terms = object_model.publish_terms.terms if object_model.publish_terms else None
        if not terms:
            continue

        for term in terms:
            if term.services and Services.auction in term.services:
                offer_ids.append(object_model.id)
                break

    if not offer_ids:
        return {}

    result = await get_auction_bets_degradation_handler(offer_ids)

    return result.value
