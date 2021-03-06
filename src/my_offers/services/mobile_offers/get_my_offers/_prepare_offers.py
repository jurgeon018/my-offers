from datetime import datetime
from operator import attrgetter
from typing import List, Optional, Set, Union

from my_offers import enums
from my_offers.entities.mobile_offer import MobOffer, MobPrice, OfferStats
from my_offers.enums import MobStatus
from my_offers.helpers import get_available_actions, is_archived, is_manual
from my_offers.helpers.category import get_types
from my_offers.helpers.fields import get_main_photo_url
from my_offers.helpers.price import get_price_info
from my_offers.helpers.similar import is_offer_for_similar
from my_offers.helpers.title import get_mobile_offer_title
from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel, PublishTerms
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Status
from my_offers.repositories.monolith_cian_announcementapi.entities.publish_term import Services
from my_offers.services.offer_view.fields import get_expiration_date_for_mobile
from my_offers.services.offer_view.fields.geo import get_address_for_push
from my_offers.services.offers.enrich.enrich_data import MobileEnrichData
from my_offers.services.offers.enrich.load_enrich_data import load_mobile_enrich_data
from my_offers.services.offers.enrich.prepare_enrich_params import prepare_enrich_params


def _parse_services(terms: Optional[PublishTerms]) -> List[enums.OfferServices]:
    result: Set[enums.OfferServices] = set()

    if not terms or not terms.terms:
        return list(result)

    for term in terms.terms:
        if not term.services:
            continue
        for service in term.services:
            try:
                result.add(enums.OfferServices[service.name])
            except KeyError:
                continue

    return sorted(list(result), key=attrgetter('name'))


async def prepare_offers(
        *,
        user_id: int,
        object_models: List[ObjectModel],
        tab_type: Union[enums.MobTabTypeV1, enums.MobTabTypeV2],
) -> List[MobOffer]:
    # получение данных для обогащения
    enrich_params = prepare_enrich_params(models=object_models, user_id=user_id)
    enrich_data = await load_mobile_enrich_data(params=enrich_params, tab_type=tab_type)

    return [
        _prepare_offer(object_model=object_model, enrich_data=enrich_data)
        for object_model in object_models
    ]


def _prepare_offer(*, object_model: ObjectModel, enrich_data: MobileEnrichData) -> MobOffer:
    offer_id = object_model.id
    offer_type, deal_type = get_types(object_model.category)
    manual = is_manual(object_model.source)
    archived = is_archived(object_model.flags)
    force_raise = bool(
        enrich_data.get_duplicates_counts(offer_id)
        or enrich_data.get_same_building_counts(offer_id)
    )
    agent_hierarchy_data = enrich_data.agent_hierarchy_data
    price_info = get_price_info(object_model)
    services: List[Services] = _parse_services(object_model.publish_terms)

    return MobOffer(
        offer_id=offer_id,
        cian_id=object_model.cian_id,
        cian_user_id=object_model.cian_user_id,
        realty_user_id=object_model.user_id,
        price=MobPrice(value=object_model.bargain_terms.price, currency=object_model.bargain_terms.currency),
        category=object_model.category,
        status=MobStatus[object_model.status.name],
        publish_till_date=get_expiration_date_for_mobile(object_model.publish_terms),
        complaints=enrich_data.get_offer_offence(offer_id),
        offer_type=offer_type,
        deal_type=deal_type,
        is_archived=archived,
        archived_date=object_model.archived_date,
        photo=get_main_photo_url(object_model.photos, better_quality=True),
        has_video_offence=offer_id in enrich_data.video_offences,
        has_photo_offence=offer_id in enrich_data.image_offences,
        is_object_on_premoderation=enrich_data.on_premoderation(offer_id),
        identification_pending=enrich_data.wait_identification(offer_id),
        is_auction=Services.auction in services,
        auction=enrich_data.get_offer_auction(offer_id),
        deactivated_service=enrich_data.get_deactivated_service(offer_id),
        formatted_price=str(price_info),
        formatted_info=get_mobile_offer_title(object_model=object_model),
        formatted_address=get_address_for_push(object_model.geo),
        stats=OfferStats(
            competitors_count=enrich_data.get_total_similar_count(offer_id),
            duplicates_count=enrich_data.get_duplicates_counts(offer_id),
            calls_count=enrich_data.get_calls_count(offer_id),
            skipped_calls_count=enrich_data.get_missed_calls_count(offer_id),
            total_views=enrich_data.get_views_total_counts(offer_id),
            daily_views=enrich_data.get_views_daily_counts(offer_id),
            favorites=enrich_data.favorites_counts.get(offer_id),
        ),
        services=services,
        description=object_model.description,
        coworking_id=object_model.coworking.id if object_model.coworking else None,
        is_private_agent=agent_hierarchy_data.is_agent,
        available_actions=get_available_actions(
            status=object_model.status,
            is_archived=archived,
            is_manual=manual,
            can_update_edit_date=enrich_data.can_update_edit_dates.get(offer_id, False),
            agency_settings=enrich_data.agency_settings,
            is_in_hidden_base=object_model.is_in_hidden_base,
            agent_hierarchy_data=agent_hierarchy_data,
            force_raise=force_raise,
            can_view_similar_offers=is_offer_for_similar(
                status=object_model.status,
                category=object_model.category,
            ),
            payed_by=enrich_data.offers_payed_by.get(offer_id)
        ),
        is_declined=object_model.status in (Status.refused, Status.removed_by_moderator)
    )
