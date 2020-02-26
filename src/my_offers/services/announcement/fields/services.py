from typing import List, Optional

from my_offers.repositories.monolith_cian_announcementapi.entities import PublishTerms
from my_offers.repositories.monolith_cian_announcementapi.entities.publish_term import Services


def get_services(publish_terms: Optional[PublishTerms]) -> List[Services]:
    result: List[Services] = []
    if not publish_terms:
        return result

    if not publish_terms.terms:
        return result

    for term in publish_terms.terms:
        if not term.services:
            continue
        for service in term.services:
            result.append(service)

    return result
