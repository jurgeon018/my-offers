from my_offers import entities
from my_offers.helpers.category import get_types
from my_offers.helpers.fields import get_main_photo_url, get_price_info
from my_offers.helpers.title import get_properties
from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel
from my_offers.repositories.postgresql.object_model import get_offers_by_ids
from my_offers.services.offer_view import fields


async def get_offers_for_calltracking(
        request: entities.OffersForCalltrackingRequest
) -> entities.OffersForCalltrackingResponse:
    """ АПИ для списка звонков - только id и фото """
    object_models = await get_offers_by_ids(request.offer_ids)

    return entities.OffersForCalltrackingResponse(
        offers=[_map_offer_for_calltracking(model) for model in object_models]
    )


def _map_offer_for_calltracking(object_model: ObjectModel) -> entities.OfferForCalltracking:
    return entities.OfferForCalltracking(
        offer_id=object_model.id,
        main_photo_url=get_main_photo_url(object_model.photos, better_quality=True),
    )


async def get_offers_for_calltracking_card(
        request: entities.OffersForCalltrackingRequest
) -> entities.OffersForCalltrackingCardResponse:
    """ АПИ для карточки контакта - все необходимая информация """
    object_models = await get_offers_by_ids(request.offer_ids)

    return entities.OffersForCalltrackingCardResponse(
        offers=[_map_offer_for_calltracking_card(model) for model in object_models]
    )


def _map_offer_for_calltracking_card(object_model: ObjectModel) -> entities.OfferForCalltrackingCard:
    offer_type, deal_type = get_types(object_model.category)

    return entities.OfferForCalltrackingCard(
        offer_id=object_model.id,
        main_photo_url=get_main_photo_url(object_model.photos, better_quality=True),
        properties=get_properties(object_model),
        geo=fields.prepare_geo_for_mobile(object_model.geo),
        deal_type=deal_type,
        offer_type=offer_type,
        price_info=get_price_info(
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
    )
