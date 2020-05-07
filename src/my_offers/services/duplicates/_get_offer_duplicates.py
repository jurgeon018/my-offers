from my_offers import entities, enums
from my_offers.repositories.postgresql.offers_duplicates import get_offer_duplicates
from my_offers.services import offer_view
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

    offers = [offer_view.build_duplicate_view(object_model) for object_model in object_models]

    return entities.GetOfferDuplicatesResponse(
        offers=offers,
        tabs=[
            entities.Tab(
                type=enums.DuplicateTabType.all,
                title='Все',
                count=total,
            ),
            entities.Tab(
                type=enums.DuplicateTabType.duplicate,
                title='Дубли',
                count=total,
            ),
        ],
        page=get_page_info(limit=limit, offset=offset, total=total),
        degradation={}
    )
