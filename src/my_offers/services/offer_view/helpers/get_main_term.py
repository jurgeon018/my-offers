from typing import List, Optional

from my_offers.repositories.monolith_cian_announcementapi.entities import PublishTerm
from my_offers.repositories.monolith_cian_announcementapi.entities.publish_term import Services


ADDITIONAL_SERVICE_TYPE = (
    Services.highlight,
    Services.calltracking,
    Services.auction,
)


def get_main_term(terms: Optional[List[PublishTerm]]) -> Optional[PublishTerm]:
    if not terms:
        return None

    for term in terms:
        if not term.services:
            continue

        for service in term.services:
            if service not in ADDITIONAL_SERVICE_TYPE:
                return term

    return None
