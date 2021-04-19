from simple_settings import settings

from my_offers import entities
from my_offers.helpers.similar import is_offer_for_similar
from my_offers.repositories import postgresql
from my_offers.services import offers as offers_module
from my_offers.services.similars.helpers.table import get_similar_table_suffix
from my_offers.services.similars.helpers.tabs import get_tabs


async def v1_get_offer_similars_tabs_public(
        request: entities.GetOfferDuplicatesTabsRequest,
        realty_user_id: int
) -> entities.GetOfferDuplicatesTabsResponse:
    object_model = await offers_module.load_object_model(user_id=realty_user_id, offer_id=request.offer_id)

    if not is_offer_for_similar(status=object_model.status, category=object_model.category):
        return entities.GetOfferDuplicatesTabsResponse(tabs=[])

    counter = await postgresql.get_similar_counter_by_offer_id(
        user_id=realty_user_id,
        offer_id=object_model.id,
        price_kf=settings.SIMILAR_PRICE_KF,
        room_delta=settings.SIMILAR_ROOM_DELTA,
        suffix=get_similar_table_suffix(object_model)
    )

    return entities.GetOfferDuplicatesTabsResponse(
        tabs=get_tabs(
            duplicate_count=counter.duplicates_count,
            same_building_count=counter.same_building_count,
            similar_count=counter.similar_count,
        ),
    )
