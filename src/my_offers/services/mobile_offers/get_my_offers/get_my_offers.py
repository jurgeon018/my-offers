from typing import Any, Dict, List

from my_offers import entities, enums
from my_offers.entities.page_info import MobilePageInfo
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import ObjectModel
from my_offers.repositories.monolith_cian_announcementapi.entities.bargain_terms import Currency
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category, ObjectModel
from my_offers.repositories.monolith_cian_announcementapi.entities.publish_term import Services
from my_offers.services.deactivated_service.get_deactivated_services import get_deactivated_services_degradation_handler
from my_offers.services.offences import (
    get_offers_with_media_offences_degradation_handler,
    get_unidentified_offers_degradation_handler,
)
from my_offers.services.offers import get_filters_mobile
from ._get_objects_models import get_object_models_with_pagination
from ._prepare_offers import prepare_offers


async def v1_get_my_offers_public(
        request: entities.MobileGetMyOffersRequest,
        realty_user_id: int
) -> entities.MobileGetMyOffersResponse:
    filters: Dict[str, Any] = await get_filters_mobile(
        filters=request.filters,
        user_id=realty_user_id,
        tab_type=request.tab_type,
        search_text=request.search,
    )

    object_models: List[ObjectModel]
    can_load_more: bool
    object_models, can_load_more = await get_object_models_with_pagination(
        filters=filters,
        limit=request.limit,
        offset=request.offset,
        sort_type=request.sort or enums.MobOffersSortType.update_date,
    )

    offers = await prepare_offers(user_id=realty_user_id, object_models=object_models, tab_type=request.tab_type)

    # TODO: CD-100663, CD-100665
    # pylint: disable=unused-variable
    deactivated_service: Dict[int, OfferDeactivatedService] = (await get_deactivated_services_degradation_handler(
        user_id=realty_user_id,
        offer_ids=[o.id for o in object_models if o.id]
    )).value

    return entities.MobileGetMyOffersResponse(
        page=MobilePageInfo(
            limit=request.limit,
            offset=request.offset,
            can_load_more=can_load_more
        ),
        offers=offers
    )
