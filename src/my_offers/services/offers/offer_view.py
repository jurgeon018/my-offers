from typing import List, Optional

from my_offers.entities.get_offers import GetOffer, Statistics
from my_offers.entities.offer_view_model import Address, Newbuilding, OfferGeo, PriceInfo, Subagent, Underground
from my_offers.repositories.monolith_cian_announcementapi.entities import BargainTerms, Geo, ObjectModel, PublishTerms
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category
from my_offers.repositories.monolith_cian_announcementapi.entities.publish_term import Services
from my_offers.services.announcement.process_announcement_service import CATEGORY_OFFER_TYPE_DEAL_TYPE


def build_offer_view(object_model: ObjectModel) -> GetOffer:
    """ Собирает из шарповой модели компактное представление объявления для выдачи.
    """
    main_photo_url = object_model.photos[0].mini_url if object_model.photos else None
    url_to_offer = None  # TODO: https://jira.cian.tech/browse/CD-73814

    geo = OfferGeo(
        address=_get_address(object_model.geo),
        newbuilding=_get_newbuilding(object_model.geo),
        underground=_get_underground(object_model.geo)
    )
    subagent = (
        Subagent(id=object_model.published_user_id, name='')  # TODO: https://jira.cian.tech/browse/CD-73807
        if object_model.published_user_id
        else None
    )
    source = bool(object_model.source and object_model.source.is_upload)

    return GetOffer(
        id=object_model.id,
        created_at=object_model.creation_date,
        title=object_model.title,
        main_photo_url=main_photo_url,
        url=url_to_offer,
        geo=geo,
        subagent=subagent,
        price_info=_get_price(object_model.bargain_terms, object_model.category),
        features=_get_features(object_model.bargain_terms, object_model.category),
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


def _get_price(bargain_terms: BargainTerms, category: Category) -> PriceInfo:
    deal_type = _get_deal_type(category)
    is_rent = deal_type.is_rent
    price = int(bargain_terms.price)

    # TODO: https://jira.cian.tech/browse/CD-73814
    if is_rent:
        exact_price = f'{price} ₽/мес.'
    else:
        exact_price = f'{price} ₽'

    return PriceInfo(exact_price=exact_price)


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


def _get_features(bargain_terms: BargainTerms, category: Category) -> List[str]:
    deal_type = _get_deal_type(category)
    is_sale = deal_type.is_sale
    is_rent = deal_type.is_rent
    features = []

    if is_sale:
        if bargain_terms.mortgage_allowed:
            features.append('Возможна ипотека')

        if bargain_terms.sale_type and bargain_terms.sale_type.is_free:
            features.append('Свободная продажа')

    if is_rent:
        if bargain_terms.agent_fee:
            features.append(f'Агенту: {bargain_terms.agent_fee}%')

        if bargain_terms.client_fee:
            features.append(f'Клиенту: {bargain_terms.client_fee}%')

        if bargain_terms.deposit:
            features.append(f'Залог: {bargain_terms.deposit} ₽')

    return features


def _get_underground(geo: Geo) -> Optional[Underground]:
    if not geo or not geo.undergrounds or not geo.address:
        return None

    # получаем основное метро
    undergrounds = list(filter(lambda x: x.is_default, geo.undergrounds))
    # определяем местоположение
    address = list(filter(lambda x: x.type.is_location, geo.address))

    if undergrounds and address:
        return Underground(
            search_url='',
            region_id=address[0].id,
            line_color=undergrounds[0].line_color,
            name=undergrounds[0].name
        )

    return None


def _get_newbuilding(geo: Geo) -> Optional[Newbuilding]:
    if not geo or not geo.jk:
        return None

    return Newbuilding(search_url='', name=geo.jk.name)


def _get_address(geo: Geo) -> Optional[Address]:
    if not geo or not geo.address:
        return None

    addresses = geo.address

    town = None
    district = None
    street = None
    house = None

    for address in addresses:
        if address.type:
            if address.type.is_location:
                town = address.full_name
            elif address.type.is_district:
                district = address.full_name
            elif address.type.is_street:
                street = address.full_name
            elif address.type.is_house:
                house = address.full_name

    address_name = ', '.join(filter(None, [town, district, street, house]))

    return Address(search_url='', name=address_name)


def _get_deal_type(category: Category) -> Category:
    _, deal_type = CATEGORY_OFFER_TYPE_DEAL_TYPE[category]
    return deal_type
