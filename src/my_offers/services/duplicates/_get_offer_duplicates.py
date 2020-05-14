from typing import Dict, List

from my_offers import entities, enums
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category, ObjectModel, Status
from my_offers.repositories.monolith_cian_announcementapi.entities.publish_term import Services
from my_offers.repositories.postgresql.offers_duplicates import get_offer_duplicates
from my_offers.services import offer_view
from my_offers.services.auctions import get_auction_bets_degradation_handler
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

    if not validate_offer(status=object_model.status, category=object_model.category):
        return get_empty_response(limit, offset)

    object_models, total = await get_offer_duplicates(
        offer_id=object_model.id,
        limit=limit,
        offset=offset,
    )

    if not object_models:
        return get_empty_response(limit, offset)

    auction_bets = await load_auction_bets(object_models)

    offers = [offer_view.build_duplicate_view(object_model, auction_bets) for object_model in object_models]

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


def get_empty_response(limit: int, offset: int) -> entities.GetOfferDuplicatesResponse:
    return entities.GetOfferDuplicatesResponse(
        offers=[],
        tabs=[],
        page=get_page_info(limit=limit, offset=offset, total=0),
    )


def validate_offer(*, status: Status, category: Category) -> bool:
    """
    Дубли делаем только для квартир и комнат во вторичке.
    Длительная аренда и продажа (без посуточной)
    """
    if not status.is_published:
        return False

    return category in CATEGORY_FOR_DUPLICATE


async def load_auction_bets(object_models: List[ObjectModel]) -> Dict[int, int]:
    offer_ids = []
    for object_model in object_models:
        terms = object_model.publish_terms.terms if object_model.publish_terms else None
        if not terms:
            continue

        for term in terms:
            if term.services and Services.auction in term.services:
                offer_ids.append(object_model.id)
                break

    if not offer_ids:
        return {}

    return await get_auction_bets_degradation_handler(offer_ids)
