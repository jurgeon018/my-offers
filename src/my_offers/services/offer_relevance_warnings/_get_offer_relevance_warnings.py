from typing import Dict, List

from cian_core.degradation import get_degradation_handler

from my_offers.entities.offer_relevance_warning import OfferRelevanceWarningInfo
from my_offers.repositories import postgresql


async def get_offer_relevance_warnings(offer_ids: List[int]) -> Dict[int, OfferRelevanceWarningInfo]:
    offer_relevance_warnings: Dict[int, OfferRelevanceWarningInfo] = {}
    repo_result = await postgresql.get_offer_relevance_warnings(offer_ids)

    for offer_relevance_warning in repo_result:
        offer_relevance_warnings[offer_relevance_warning.offer_id] = offer_relevance_warning

    return offer_relevance_warnings


get_offer_relevance_warnings_degradation_handler = get_degradation_handler(
    func=get_offer_relevance_warnings,
    key='psql.get_offer_relevance_warnings',
    default={},
)
