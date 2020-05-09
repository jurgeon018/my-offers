from my_offers import entities, enums
from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category
from my_offers.repositories.postgresql.offers_duplicates import get_offer_duplicates
from my_offers.services import offer_view
from my_offers.services.offers import get_page_info, get_pagination, load_object_model


CATEGORY_FOR_DUPLICATE = (
    Category.flat_sale,
    Category.room_sale,
    Category.flat_rent,
    Category.room_rent,
)


async def v1_get_offer_duplicates_public(
        request: entities.GetOfferDuplicatesRequest,
        realty_user_id: int
) -> entities.GetOfferDuplicatesResponse:
    object_model = await load_object_model(user_id=realty_user_id, offer_id=request.offer_id)
    limit, offset = get_pagination(request.pagination)

    if not validate_offer(object_model):
        return entities.GetOfferDuplicatesResponse(
            offers=[],
            tabs=[],
            page=get_page_info(limit=limit, offset=offset, total=0),
        )

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
    )


def validate_offer(object_model: ObjectModel) -> bool:
    """
    Дубли делаем только для квартир и комнат во вторичке.
    Длительная аренда и продажа (без посуточной)
    """
    if not object_model.status.is_published:
        return False

    return object_model.category in CATEGORY_FOR_DUPLICATE
