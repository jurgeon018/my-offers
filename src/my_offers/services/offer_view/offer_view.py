from typing import List, Optional

from my_offers import enums
from my_offers.entities.get_offers import GetOffer, Statistics
from my_offers.entities.offer_view_model import PriceInfo
from my_offers.repositories.monolith_cian_announcementapi.entities import BargainTerms, ObjectModel, PublishTerms
from my_offers.repositories.monolith_cian_announcementapi.entities.publish_term import Services
from my_offers.services.announcement import category
from my_offers.services.offer_view.geo import prepare_geo


async def build_offer_view(object_model: ObjectModel) -> GetOffer:
    """ Собирает из шарповой модели компактное представление объявления для выдачи."""
    main_photo_url = object_model.photos[0].mini_url if object_model.photos else None
    url_to_offer = None  # TODO: https://jira.cian.tech/browse/CD-73814

    subagent = None  # TODO: https://jira.cian.tech/browse/CD-73807
    source = bool(object_model.source and object_model.source.is_upload)

    offer_type, deal_type = category.get_types(object_model.category)

    return GetOffer(
        id=object_model.id,
        created_at=object_model.creation_date,
        title=object_model.title,
        main_photo_url=main_photo_url,
        url=url_to_offer,
        geo=await prepare_geo(geo=object_model.geo, deal_type=deal_type, offer_type=offer_type),
        subagent=subagent,
        price_info=_get_price(bargain_terms=object_model.bargain_terms, deal_type=deal_type),
        features=_get_features(bargain_terms=object_model.bargain_terms, deal_type=deal_type),
        publish_features=_get_publish_features(object_model.publish_terms),
        vas=_get_vas(object_model.publish_terms),
        is_from_package=_is_from_package(object_model.publish_terms),
        is_manual=source,
        is_publication_time_ends=_is_publication_time_ends(object_model),
        statistics=Statistics()
    )


def _is_publication_time_ends(raw_offer: ObjectModel) -> bool:
    # TODO: https://jira.cian.tech/browse/CD-73814
    return False


def _is_from_package(publish_terms: PublishTerms) -> bool:
    if not publish_terms or not publish_terms.terms:
        return False

    # publish_terms только для опубликованных
    return any(
        term.tariff_identificator.tariff_grid_type.is_service_package
        for term in publish_terms.terms
        if term.tariff_identificator and term.tariff_identificator.tariff_grid_type
    )


def _get_vas(publish_terms: PublishTerms) -> Optional[List[Services]]:
    if not publish_terms or not publish_terms.terms:
        return None

    services: List[Services] = []
    for t in publish_terms.terms:
        if t.services:
            services.extend(t.services)

    return services


def _get_price(*, bargain_terms: BargainTerms, deal_type: enums.DealType) -> PriceInfo:
    price = int(bargain_terms.price)

    # TODO: https://jira.cian.tech/browse/CD-73814
    if deal_type.is_rent:
        exact = f'{price} ₽/мес.'
    else:
        exact = f'{price} ₽'

    return PriceInfo(exact=exact)


def _get_publish_features(publish_terms: PublishTerms) -> Optional[List[str]]:
    if not publish_terms:
        return None

    features = []

    if publish_terms.autoprolong:
        features.append('автопродление')

    if publish_terms.terms:
        days = publish_terms.terms[0].days
        features.append(f'осталось {days} д.')  # TODO: https://jira.cian.tech/browse/CD-73814

    return features


def _get_features(*, bargain_terms: BargainTerms, deal_type: enums.DealType) -> List[str]:
    features = []

    if deal_type.is_sale:
        if bargain_terms.mortgage_allowed:
            features.append('Возможна ипотека')

        if bargain_terms.sale_type and bargain_terms.sale_type.is_free:
            features.append('Свободная продажа')
    else:
        if bargain_terms.agent_fee:
            features.append(f'Агенту: {bargain_terms.agent_fee}%')

        if bargain_terms.client_fee:
            features.append(f'Клиенту: {bargain_terms.client_fee}%')

        if bargain_terms.deposit:
            features.append(f'Залог: {bargain_terms.deposit} ₽')

    return features
