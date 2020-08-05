from typing import List

from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel
from my_offers.repositories.monolith_cian_announcementapi.entities.publish_term import Services


def get_offers_ids_with_auction(object_models: List[ObjectModel]) -> List[int]:
    offer_ids = []
    for object_model in object_models:
        terms = object_model.publish_terms.terms if object_model.publish_terms else None
        if not terms:
            continue

        for term in terms:
            if term.services and Services.auction in term.services:
                offer_ids.append(object_model.id)
                break

    return offer_ids
