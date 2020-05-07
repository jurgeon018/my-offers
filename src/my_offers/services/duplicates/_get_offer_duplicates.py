from my_offers import entities
from my_offers.repositories.postgresql.offers_duplicates import get_offer_duplicates
from my_offers.services.offers import get_page_info, get_pagination, load_object_model


async def v1_get_offer_duplicates_public(
        request: entities.GetOfferDuplicatesRequest,
        realty_user_id: int
) -> entities.GetOfferDuplicatesResponse:
    object_model = await load_object_model(user_id=realty_user_id, offer_id=request.offer_id)
    limit, offset = get_pagination(request.pagination)

    object_models, total = await get_offer_duplicates(
        offer_id=object_model.id,
        limit=limit,
        offset=offset,
    )

    return entities.GetOfferDuplicatesResponse(
        offers=[],
        tabs=[],
        page=get_page_info(limit=limit, offset=offset, total=total),
        degradation={}
    )
