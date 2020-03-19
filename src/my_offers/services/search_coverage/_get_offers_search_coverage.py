from datetime import datetime, timedelta
from typing import Dict, List

import pytz
from cian_core.degradation import get_degradation_handler
from simple_settings import settings

from my_offers import entities
from my_offers.repositories.search_coverage import v1_get_offers_search_coverage
from my_offers.repositories.search_coverage.entities import OffersCoverageRequest


async def get_offers_search_coverage(offer_ids: List[int]) -> Dict[int, entities.Coverage]:
    now = datetime.now(tz=pytz.UTC)
    date_from = now.date()
    date_to = (now - timedelta(days=settings.DAYS_FOR_COVERAGE)).date()

    response = await v1_get_offers_search_coverage(
        OffersCoverageRequest(
            offer_ids=offer_ids,
            date_from=date_from,
            date_to=date_to,
        )
    )
    result = {}
    for item in response.data:
        result[item.offer_id] = entities.Coverage(
            searches_count=item.searches_count,
            shows_count=item.shows_count,
            coverage=item.coverage,
        )

    return result


get_offers_search_coverage_degradation_handler = get_degradation_handler(
    func=get_offers_search_coverage,
    key='get_offers_search_coverage',
    default={},
)
