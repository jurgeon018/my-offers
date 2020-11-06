from typing import Dict

from my_offers import entities, enums
from my_offers.helpers.category import get_types
from my_offers.helpers.fields import (
    get_locations,
    get_main_photo_url,
    get_price_info,
    get_price_info_with_trend,
    get_sort_date,
)
from my_offers.helpers.status_tab import get_status_tab
from my_offers.helpers.title import get_offer_title, get_properties
from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel
from my_offers.services.offer_view import fields


def build_duplicate_view(
        *,
        object_model: ObjectModel,
        auction_bets: Dict[int, float],
        similar: entities.OfferSimilarWithType,
) -> entities.OfferDuplicate:
    offer_type, deal_type = get_types(object_model.category)
    status_tab = get_status_tab(offer_flags=object_model.flags, offer_status=object_model.status)

    realty_offer_id = object_model.id
    return entities.OfferDuplicate(
        offer_id=realty_offer_id,
        deal_type=deal_type,
        offer_type=offer_type,
        main_photo_url=get_main_photo_url(object_model.photos, better_quality=True),
        properties=get_properties(object_model),
        geo=fields.prepare_geo_for_mobile(object_model.geo),
        display_date=get_sort_date(object_model=object_model, status_tab=status_tab),
        price_info=get_price_info_with_trend(
            locations=get_locations(object_model.geo),
            bargain_terms=object_model.bargain_terms,
            category=object_model.category,
            can_parts=bool(object_model.can_parts),
            min_area=object_model.min_area,
            max_area=object_model.max_area,
            total_area=object_model.total_area,
            offer_type=offer_type,
            deal_type=deal_type,
            coworking_offer_type=object_model.coworking_offer_type,
            workplace_count=object_model.workplace_count,
            old_price=similar.old_price
        ),
        vas=fields.get_vas(object_model.publish_terms.terms if object_model.publish_terms else None),
        auction_bet=fields.get_auction_bet(auction_bets.get(realty_offer_id)),
        type=similar.similar_type,
    )


def build_duplicate_view_desktop(
        *,
        object_model: ObjectModel,
        auction_bets: Dict[int, float],
        duplicate_type: enums.DuplicateType = enums.DuplicateType.duplicate,
) -> entities.OfferDuplicateDesktop:
    offer_type, deal_type = get_types(object_model.category)
    status_tab = get_status_tab(offer_flags=object_model.flags, offer_status=object_model.status)
    realty_offer_id = object_model.id

    return entities.OfferDuplicateDesktop(
        offer_id=realty_offer_id,
        url=fields.get_offer_url(
            cian_offer_id=object_model.cian_id,
            deal_type=deal_type,
            offer_type=offer_type
        ),
        title=get_offer_title(object_model),
        main_photo_url=get_main_photo_url(object_model.photos),
        geo=fields.prepare_geo_for_mobile(object_model.geo),
        display_date=get_sort_date(object_model=object_model, status_tab=status_tab),
        price_info=get_price_info(
            locations=get_locations(object_model.geo),
            bargain_terms=object_model.bargain_terms,
            category=object_model.category,
            can_parts=bool(object_model.can_parts),
            min_area=object_model.min_area,
            max_area=object_model.max_area,
            total_area=object_model.total_area,
            offer_type=offer_type,
            deal_type=deal_type,
            coworking_offer_type=object_model.coworking_offer_type,
            workplace_count=object_model.workplace_count,
        ),
        vas=fields.get_vas(object_model.publish_terms.terms if object_model.publish_terms else None),
        auction_bet=fields.get_auction_bet(auction_bets.get(realty_offer_id)),
        type=duplicate_type,
    )
