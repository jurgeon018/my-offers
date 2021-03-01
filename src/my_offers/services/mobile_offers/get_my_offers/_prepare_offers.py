import asyncio
from asyncio.tasks import Task
from datetime import datetime
from typing import Dict, List, Mapping, Optional, Set

from cian_core.degradation import DegradationResult

from my_offers.entities import AvailableActions, OfferSimilarCounter
from my_offers.entities.mobile_offer import (
    ConcurrencyType, MobOffer,
    MobPrice,
    OfferAuction,
    OfferComplaint,
    OfferDeactivatedService,
    OfferStats,
)
from my_offers.entities.moderation import OfferOffence
from my_offers.enums import MobStatus
from my_offers.helpers import is_archived
from my_offers.helpers.category import get_types
from my_offers.helpers.fields import get_main_photo_url
from my_offers.helpers.price import get_price_info
from my_offers.repositories.auction.entities import GetMobileBetAnnouncementsInfoResponse
from my_offers.repositories.callbook.entities import OfferCallCount
from my_offers.repositories.moderation.entities import (
    GetImageOffencesForAnnouncementsResponse,
    GetVideoOffencesForAnnouncementsResponse,
)
from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel, PublishTerms
from my_offers.repositories.monolith_cian_announcementapi.entities.publish_term import Services
from my_offers.services.favorites import get_favorites_counts_degradation_handler
from my_offers.services.offer_view.fields.geo import get_address_for_push


def _parse_offences_to_complaint(offences: List[OfferOffence]) -> Mapping[int, List[OfferComplaint]]:
    result: Dict[int, List[OfferComplaint]] = {}

    for offence_item in offences:
        complaint: OfferComplaint = OfferComplaint(
            id=offence_item.offence_id,
            date=offence_item.created_date,
            comment=offence_item.offence_text,
        )
        if offence_item.offer_id not in result:
            result[offence_item.offer_id] = [complaint]
        else:
            result[offence_item.offer_id].append(complaint)

    return result


def _parse_auctions(auctions: GetMobileBetAnnouncementsInfoResponse) -> Mapping[int, OfferAuction]:
    result: Dict[int, OfferAuction] = {}

    for auction_item in auctions.announcements:
        concurrency_types: List[ConcurrencyType] = []

        for c_t in auction_item.concurrency_types:
            concurrency_types.append(ConcurrencyType(
                is_active=c_t.is_active,
                name=c_t.name,
                type=c_t.type.value
            ))

        auction: OfferAuction = OfferAuction(
            increase_bets_positions_count=auction_item.increase_bets_positions_count,
            current_bet=auction_item.current_bet,
            note_bet=auction_item.note_bet,
            is_available_auction=auction_item.is_available_auction,
            concurrency_types=concurrency_types,
            is_strategy_enabled=auction_item.is_strategy_enabled,
            is_fixed_bet=auction_item.is_fixed_bet,
            strategy_description=auction_item.strategy_description,
            concurrency_type_title=auction_item.concurrency_type_title,
        )
        result[auction_item.announcement_id] = auction

    return result


def _parse_services(terms: Optional[PublishTerms]) -> List[Services]:
    result: Set[Services] = set()

    if not terms or not terms.terms:
        return list(result)

    for term in terms.terms:
        if not term.services:
            continue
        for service in term.services:
            result.add(service)

    return list(result)


async def prepare_data_for_mobile_offers(
        object_models: List[ObjectModel],
        publish_tills: Mapping[int, datetime],
        offer_offences: List[OfferOffence],
        image_offence: GetImageOffencesForAnnouncementsResponse,
        video_offence: GetVideoOffencesForAnnouncementsResponse,
        deactivated_service: Mapping[int, OfferDeactivatedService],
        premoderation_offers: List[int],
        offers_with_pending_identification: List[int],
        offers_auctions: GetMobileBetAnnouncementsInfoResponse,
        similar_counters: List[OfferSimilarCounter],
        calls_counts: List[OfferCallCount],
) -> List[MobOffer]:
    result: List[MobOffer] = []

    favorites_counts_task: Task[DegradationResult[Mapping[int, int]]] = asyncio.create_task(
        get_favorites_counts_degradation_handler([o.id for o in object_models])
    )

    complaints: Mapping[int, List[OfferComplaint]] = _parse_offences_to_complaint(offer_offences)

    auctions: Mapping[int, OfferAuction] = _parse_auctions(offers_auctions)

    similar: Mapping[int, OfferSimilarCounter] = {s.offer_id: s for s in similar_counters}

    raw_calls_counts: Mapping[int, OfferCallCount] = {c.offer_id: c for c in calls_counts}

    offers_with_image_offence: List[int] = [o.announcement_id for o in image_offence.items]
    offers_with_video_offence: List[int] = [o.announcement_id for o in video_offence.items]

    favorites_counts: Mapping[int, int] = (await favorites_counts_task).value

    for obj_model in object_models:
        realty_offer_id = obj_model.id

        offer_type, deal_type = get_types(obj_model.category)
        archived = is_archived(obj_model.flags)

        competitors_count = similar[realty_offer_id].total_count if realty_offer_id in similar_counters else None
        duplicates_count = similar[realty_offer_id].duplicates_count if realty_offer_id in similar_counters else None

        calls: Optional[OfferCallCount] = raw_calls_counts.get(realty_offer_id)

        services: List[Services] = _parse_services(obj_model.publish_terms)

        result.append(MobOffer(
            offer_id=realty_offer_id,
            price=MobPrice(value=obj_model.bargain_terms.price, currency=obj_model.bargain_terms.currency),
            category=obj_model.category,
            status=MobStatus[obj_model.status.name],
            publish_till_date=publish_tills.get(realty_offer_id),
            complaints=complaints.get(realty_offer_id),
            offer_type=offer_type,
            deal_type=deal_type,
            is_archived=archived,
            archived_date=obj_model.archived_date,
            photo=get_main_photo_url(obj_model.photos, better_quality=True),
            has_video_offence=realty_offer_id in offers_with_video_offence,
            has_photo_offence=realty_offer_id in offers_with_image_offence,
            deactivated_service=deactivated_service.get(realty_offer_id),
            is_object_on_premoderation=realty_offer_id in premoderation_offers,
            identification_pending=realty_offer_id in offers_with_pending_identification,
            is_auction=Services.auction in services,
            auction=auctions.get(realty_offer_id),
            formatted_price=get_price_info(obj_model).exact,
            formatted_info='CHANGEME',  # Не сделано
            formatted_address=get_address_for_push(obj_model.geo),
            stats=OfferStats(
                competitors_count=competitors_count,
                duplicates_count=duplicates_count,
                calls_count=calls.calls_count if calls else None,
                skipped_calls_count=calls.missed_calls_count if calls else None,
                total_views=None,  # Не сделано
                daily_views=None,  # Не сделано
                favorites=favorites_counts.get(realty_offer_id),
            ),
            services=services,
            description=obj_model.description,
            coworking_id=123,  # Не сделано
            is_private_agent=False,  # Не сделано
            available_actions=AvailableActions(  # Не сделано
                can_edit=True,
                can_restore=True,
                can_update_edit_date=True,
                can_move_to_archive=True,
                can_delete=True,
                can_raise=True,
                can_raise_without_addform=True,
                can_change_publisher=True,
                can_view_similar_offers=True,

            ),
        ))

    return result
