from simple_settings import settings

from my_offers import enums
from my_offers.entities.get_offers import GetOffer, Statistics
from my_offers.helpers.category import get_types
from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel
from my_offers.services.offer_view.fields import (
    get_available_actions,
    get_features,
    get_moderation,
    get_not_active_info,
    get_price_info,
    get_publish_features,
    get_status,
    get_title,
    get_vas,
    is_from_package,
    prepare_geo,
)
from my_offers.services.offers.enrich.enrich_data import EnrichData


def build_offer_view(*, object_model: ObjectModel, enrich_data: EnrichData) -> GetOffer:
    """ Собирает из шарповой модели компактное представление объявления для выдачи."""
    offer_type, deal_type = get_types(object_model.category)
    main_photo_url = object_model.photos[0].mini_url if object_model.photos else None
    url_to_offer = _get_offer_url(
        offer_id=object_model.id,
        offer_type=offer_type,
        deal_type=deal_type
    )
    subagent = None  # TODO: https://jira.cian.tech/browse/CD-73807
    is_manual = bool(object_model.source and object_model.source.is_upload)
    is_archived = bool(object_model.flags and object_model.flags.is_archived)
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
    publish_terms = object_model.publish_terms
    terms = publish_terms.terms if publish_terms else None
    geo_urls = enrich_data.get_urls_by_types(deal_type=deal_type, offer_type=offer_type)
    moderation = get_moderation(
        status=object_model.status,
        offer_offence=enrich_data.get_offer_offence(offer_id=object_model.id)
    )

    return GetOffer(
        id=object_model.id,
        created_at=object_model.creation_date,
        title=get_title(object_model),
        main_photo_url=main_photo_url,
        url=url_to_offer,
        geo=prepare_geo(geo=object_model.geo, geo_urls=geo_urls, jk_urls=enrich_data.jk_urls),
        subagent=subagent,
        price_info=price_info,
        features=features,
        publish_features=get_publish_features(publish_terms),
        vas=get_vas(terms),
        is_from_package=is_from_package(terms),
        is_manual=is_manual,
        is_publication_time_ends=_is_publication_time_ends(object_model),
        statistics=Statistics(),
        archived_at=object_model.archived_date,
        status=get_status(status=object_model.status, is_archived=is_archived),
        available_actions=get_available_actions(
            status=object_model.status,
            is_archived=is_archived,
            is_manual=is_manual,
            can_update_edit_date=enrich_data.can_update_edit_dates.get(object_model.id, False),
        ),
        not_active_info=get_not_active_info(
            status=object_model.status,
            import_error=enrich_data.import_errors.get(object_model.id),
            edit_date=object_model.edit_date
        ),
        moderation=moderation,
    )


def _get_offer_url(
        *,
        offer_id: int,
        offer_type: enums.OfferType,
        deal_type: enums.DealType
) -> str:
    return f'{settings.CiAN_BASE_URL}/{deal_type.value}/{offer_type.value}/{offer_id}'


def _is_publication_time_ends(raw_offer: ObjectModel) -> bool:
    # TODO: https://jira.cian.tech/browse/CD-74186
    return False
