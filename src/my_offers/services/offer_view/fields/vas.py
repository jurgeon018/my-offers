from typing import List, Optional

from my_offers import enums
from my_offers.repositories.monolith_cian_announcementapi.entities.publish_term import PublishTerm, Services


SERVICE_VAS_MAP = {
    Services.top3: enums.OfferVas.top3,
    Services.auction: enums.OfferVas.auction,
    Services.premium: enums.OfferVas.premium,
    Services.paid: enums.OfferVas.payed,
    Services.highlight: enums.OfferVas.colorized,
}


def get_vas(terms: Optional[List[PublishTerm]]) -> List[enums.OfferVas]:
    result: List[enums.OfferVas] = []

    if not terms:
        return result

    for term in terms:
        if not term.services:
            continue

        for service in term.services:
            if vas := SERVICE_VAS_MAP.get(service):
                result.append(vas)

    return result
