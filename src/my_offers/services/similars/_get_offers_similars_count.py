from simple_settings import settings

from my_offers import entities
from my_offers.repositories.postgresql.object_model import get_object_model_by_id
from my_offers.repositories.postgresql.offers_similars import get_similars_counters_by_offer_ids
from my_offers.services.similars.helpers.table import get_similar_table_suffix


async def v1_get_offers_similars_count(
        request: entities.GetOffersDuplicatesCountRequest
) -> entities.GetOffersDuplicatesCountResponse:
    offer_ids = request.offer_ids
    if not offer_ids:
        return entities.GetOffersDuplicatesCountResponse(
            data=[]
        )

    object_model = await get_object_model_by_id(offer_ids[0])
    if not object_model:
        return entities.GetOffersDuplicatesCountResponse(
            data=[]
        )
    suffix = get_similar_table_suffix(object_model)

    counters = await get_similars_counters_by_offer_ids(
        user_id=object_model.published_user_id,
        offer_ids=offer_ids,
        price_kf=settings.SIMILAR_PRICE_KF,
        room_delta=settings.SIMILAR_ROOM_DELTA,
        suffix=suffix,
    )

    return entities.GetOffersDuplicatesCountResponse(data=[_map_counter(counter) for counter in counters])


def _map_counter(counter: entities.OfferSimilarCounter) -> entities.OfferDuplicatesCount:
    duplicates_count = counter.duplicates_count if counter.duplicates_count else None
    competitors_count = counter.duplicates_count + counter.same_building_count
    competitors_count = competitors_count if competitors_count else None

    return entities.OfferDuplicatesCount(
        offer_id=counter.offer_id,
        competitors_count=competitors_count,
        duplicates_count=duplicates_count,
    )
