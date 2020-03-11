from typing import List, Optional

from my_offers.repositories.monolith_cian_announcementapi.entities import PublishTerm


def is_from_package(terms: Optional[List[PublishTerm]]) -> bool:
    if not terms:
        return False

    for term in terms:
        if not term.tariff_identificator:
            continue

        if grid_type := term.tariff_identificator.tariff_grid_type:
            if grid_type.is_service_package_group:
                return True

    return False
