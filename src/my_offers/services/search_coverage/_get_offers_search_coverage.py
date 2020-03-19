from typing import Dict, List

from cian_core.degradation import get_degradation_handler

from my_offers import entities


async def get_offers_search_coverage(offer_ids: List[int]) -> Dict[int, entities.Coverage]:
    data = []
    coverage = {item.offer_id: item for item in data}

    result = {}
    for offer_id in offer_ids:
        if offer_id in coverage:
            item = coverage[offer_id]
            result[offer_id] = entities.Coverage(
                searches_count=item.searches_count,
                shows_count=item.shows_count,
                coverage=item.coverage,
            )
        else:
            result[offer_id] = entities.Coverage(
                searches_count=0,
                shows_count=0,
                coverage=0,
            )

    return result


get_offers_search_coverage_degradation_handler = get_degradation_handler(
    func=get_offers_search_coverage,
    key='get_offers_search_coverage',
    default={},
)
