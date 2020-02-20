from simple_settings import settings

from my_offers import enums
from my_offers.entities.get_offers import GetOffer, Statistics
from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel
from my_offers.services.announcement.category import get_types
from my_offers.services.offer_view.fields.features import get_features
from my_offers.services.offer_view.fields.geo import prepare_geo
from my_offers.services.offer_view.fields.is_from_package import is_from_package
from my_offers.services.offer_view.fields.price_info import get_price_info
from my_offers.services.offer_view.fields.publish_features import get_publish_features
from my_offers.services.offer_view.fields.title import get_title
from my_offers.services.offer_view.fields.vas import get_vas


async def build_offer_view(object_model: ObjectModel) -> GetOffer:
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

    return GetOffer(
        id=object_model.id,
        created_at=object_model.creation_date,
        title=get_title(object_model),
        main_photo_url=main_photo_url,
        url=url_to_offer,
        geo=await prepare_geo(geo=object_model.geo, deal_type=deal_type, offer_type=offer_type),
        subagent=subagent,
        price_info=price_info,
        features=features,
        publish_features=get_publish_features(publish_terms),
        vas=get_vas(terms),
        is_from_package=is_from_package(terms),
        is_manual=is_manual,
        is_publication_time_ends=_is_publication_time_ends(object_model),
        statistics=Statistics()
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
