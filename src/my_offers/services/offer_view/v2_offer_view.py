from my_offers.entities import get_offers
from my_offers.helpers.category import get_types
from my_offers.helpers.fields import is_archived
from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel
from my_offers.services.offer_view.fields import (
    get_available_actions,
    get_features,
    get_offer_url,
    get_price_info,
    get_status,
    get_title,
    prepare_geo,
)
from my_offers.services.offer_view.fields.page_specific_info import get_page_specific_info
from my_offers.services.offers.enrich.enrich_data import EnrichData


def v2_build_offer_view(
        *,
        object_model: ObjectModel,
        enrich_data: EnrichData,
) -> get_offers.GetOfferV2:
    """ Собирает из шарповой модели компактное представление объявления для выдачи."""
    offer_type, deal_type = get_types(object_model.category)
    main_photo_url = object_model.photos[0].mini_url if object_model.photos else None
    subagent = None  # TODO: https://jira.cian.tech/browse/CD-73807
    is_manual = bool(object_model.source and object_model.source.is_upload)
    archived = is_archived(object_model.flags)
    price_info = get_price_info(
        bargain_terms=object_model.bargain_terms,
        category=object_model.category,
        can_parts=bool(object_model.can_parts),
        min_area=object_model.min_area,
        max_area=object_model.max_area,
        total_area=object_model.total_area,
        offer_type=offer_type,
        deal_type=deal_type
    )
    features = get_features(
        bargain_terms=object_model.bargain_terms,
        category=object_model.category,
        total_area=object_model.total_area,
        offer_type=offer_type,
        deal_type=deal_type
    )
    geo_urls = enrich_data.get_urls_by_types(deal_type=deal_type, offer_type=offer_type)

    return get_offers.GetOfferV2(
        id=object_model.id,
        created_at=object_model.creation_date,
        title=get_title(object_model),
        main_photo_url=main_photo_url,
        url=get_offer_url(offer_id=object_model.id, offer_type=offer_type, deal_type=deal_type),
        geo=prepare_geo(geo=object_model.geo, geo_urls=geo_urls, jk_urls=enrich_data.jk_urls),
        subagent=subagent,
        price_info=price_info,
        features=features,
        is_manual=is_manual,
        statistics=get_offers.Statistics(),
        archived_at=object_model.archived_date,
        status=get_status(status=object_model.status, is_archived=archived),
        available_actions=get_available_actions(
            status=object_model.status,
            is_archived=archived,
            is_manual=is_manual,
            can_update_edit_date=enrich_data.can_update_edit_dates.get(object_model.id, False),
        ),
        page_specific_info=get_page_specific_info(
            object_model=object_model,
            enrich_data=enrich_data,
        ),
    )
