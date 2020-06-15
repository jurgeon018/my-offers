from cian_core.degradation import get_degradation_handler
from cian_web.exceptions import BrokenRulesException, Error

from my_offers import entities
from my_offers.helpers.category import get_types
from my_offers.repositories.price_estimator import v1_get_estimation_for_realtors
from my_offers.repositories.price_estimator.entities import (
    GetEstimationForRealtorsRequest,
    GetEstimationForRealtorsResponse,
)
from my_offers.services.convert_price import get_price_rur
from my_offers.services.offers import load_object_model
from my_offers.services.valuation.fields.address import get_address
from my_offers.services.valuation.fields.house_id import get_house_id
from my_offers.services.valuation.fields.info_relative_market import get_info_relative_market
from my_offers.services.valuation.fields.rooms_count import get_rooms_count
from my_offers.services.valuation.helpers.validation_offer import validate_offer
from my_offers.services.valuation.helpers.valuation_filters import get_valuation_filters
from my_offers.services.valuation.helpers.valuation_option import get_valuation_options


async def v1_get_offer_valuation_public(
        request: entities.GetOfferValuationRequest,
        realty_user_id: int
) -> entities.GetOfferValuationResponse:
    offer_id = request.offer_id
    object_model = await load_object_model(user_id=realty_user_id, offer_id=offer_id)
    _, deal_type = get_types(object_model.category)

    if not validate_offer(category=object_model.category):
        raise BrokenRulesException([
            Error(
                message=f'offer category {object_model.category} is not supported',
                code='category_not_supported',
                key='offer_category'
            )
        ])

    if not object_model.geo:
        raise BrokenRulesException([
            Error(
                message='broken offer object_model, has not right geo address',
                code='valuation_not_poossible',
                key='geo'
            )
        ])

    if not object_model.bargain_terms.price:
        raise BrokenRulesException([
            Error(
                message='offer object_model has uncorrect price '
                        'valuation can not be provided without price',
                code='valuation_not_poossible',
                key='price'
            )
        ])

    price_in_rur = get_price_rur(
        price=object_model.bargain_terms.price,
        currency=object_model.bargain_terms.currency
    )

    response = await v1_get_estimation_for_realtors_degradation_handler(
        GetEstimationForRealtorsRequest(
            address=get_address(object_model.geo),
            area=object_model.total_area,
            deal_type=deal_type,
            house_id=get_house_id(object_model.geo),
            offer_id=offer_id,
            price=price_in_rur,
            rooms_count=get_rooms_count(
                category=object_model.category,
                flat_type=object_model.flat_type,
                rooms_count=object_model.rooms_count
            ),
            filters=get_valuation_filters(object_model)
        )
    )
    if response.degraded:
        raise BrokenRulesException([
            Error(
                message='mcs price-estimator degraded response',
                code='did_not_get_valuation',
                key='no_valuation'
            )
        ])
    if not response.value.prices:
        raise BrokenRulesException([
            Error(
                message='did not get valuation for offer from mcs price-estimator',
                code='did_not_get_valuation',
                key='no_valuation'
            )
        ])

    return entities.GetOfferValuationResponse(
        valuation_options=get_valuation_options(
            deal_type=deal_type,
            publish_terms=object_model.publish_terms,
            valuation_response=response.value,
        ),
        info_relative_market=get_info_relative_market(
            deal_type=deal_type,
            market_price=response.value.prices.price,
            real_price=price_in_rur,
        ),
        valuation_block_link_share=response.value.url,
        valuation_block_link_report=response.value.url,
    )


v1_get_estimation_for_realtors_degradation_handler = get_degradation_handler(
    func=v1_get_estimation_for_realtors,
    key='v1_get_estimation_for_realtors',
    default=GetEstimationForRealtorsResponse(),
)
