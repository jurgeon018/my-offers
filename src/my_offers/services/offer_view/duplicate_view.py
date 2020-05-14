from typing import Dict

from my_offers import entities, enums
from my_offers.helpers.category import get_types
from my_offers.helpers.fields import get_sort_date
from my_offers.helpers.status_tab import get_status_tab
from my_offers.helpers.title import get_properties
from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel
from my_offers.services.offer_view.fields import get_main_photo_url, get_price_info, get_vas, prepare_geo_for_mobile


def build_duplicate_view(object_model: ObjectModel, auction_bets: Dict[int, float]) -> entities.OfferDuplicate:
    offer_type, deal_type = get_types(object_model.category)
    status_tab = get_status_tab(offer_flags=object_model.flags, offer_status=object_model.status)

    offer_id = object_model.id
    return entities.OfferDuplicate(
        offer_id=offer_id,
        main_photo_url=get_main_photo_url(object_model.photos),
        properties=get_properties(object_model),
        geo=prepare_geo_for_mobile(object_model.geo),
        display_date=get_sort_date(object_model=object_model, status_tab=status_tab),
        price_info=get_price_info(
            bargain_terms=object_model.bargain_terms,
            category=object_model.category,
            can_parts=bool(object_model.can_parts),
            min_area=object_model.min_area,
            max_area=object_model.max_area,
            total_area=object_model.total_area,
            offer_type=offer_type,
            deal_type=deal_type,
        ),
        vas=get_vas(object_model.publish_terms.terms if object_model.publish_terms else None),
        auction_bet=auction_bets.get(offer_id),
        type=enums.DuplicateType.duplicate,
    )
