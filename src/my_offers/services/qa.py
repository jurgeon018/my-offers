from cian_web.exceptions import BrokenRulesException, Error

from my_offers import entities
from my_offers.entities.qa import QaGetByIdRequest
from my_offers.repositories.postgresql.object_model import get_object_model_by_id
from my_offers.repositories.postgresql.offer import get_offer_by_id
from my_offers.services.offers.get_offers_service import get_offer_views


async def get_offer(request: QaGetByIdRequest) -> entities.Offer:
    offer = await get_offer_by_id(request.offer_id)

    if not offer:
        raise BrokenRulesException([Error(message='Not found', code='not_found', key='offer_id')])

    return offer


async def get_offer_view(request: QaGetByIdRequest) -> entities.OfferViewModel:
    object_model = await get_object_model_by_id(request.offer_id)

    if not object_model:
        raise BrokenRulesException([Error(message='Not found', code='not_found', key='offer_id')])

    offers = await get_offer_views([object_model])

    return offers[0]
