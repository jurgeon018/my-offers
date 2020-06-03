from my_offers import entities
from my_offers.helpers.category import get_types
from my_offers.repositories.price_estimator import v1_get_estimation_for_realtors
from my_offers.repositories.price_estimator.entities import GetEstimationForRealtorsRequest
from my_offers.services.offers import load_object_model
from my_offers.services.valuation.fields.address import get_address
from my_offers.services.valuation.fields.house_id import get_house_id
from my_offers.services.valuation.fields.info_relative_market import get_info_relative_market
from my_offers.services.valuation.fields.price import get_price_rur
from my_offers.services.valuation.fields.rooms_count import get_rooms_count
from my_offers.services.valuation.fields.valuation_option import get_valuation_options


async def v1_get_offer_valuation_public(
        request: entities.GetOfferValuationRequest,
        realty_user_id: int
) -> entities.GetOfferValuationResponse:
    offer_id = request.offer_id
    object_model = await load_object_model(user_id=realty_user_id, offer_id=offer_id)
    _, deal_type = get_types(object_model.category)
    filters = None  # todo https://jira.cian.tech/browse/CD-82137

    price_in_rur = get_price_rur(
        price=object_model.bargain_terms.price,
        currency=object_model.bargain_terms.currency
    )

    # todo https://jira.cian.tech/browse/CD-82659
    # впилить деградацию и валидацию, что считаем оценку только для  жилой вторички - квартир и комнат
    response = await v1_get_estimation_for_realtors(
        GetEstimationForRealtorsRequest(
            address=get_address(object_model.geo.address),
            area=object_model.total_area,
            deal_type=deal_type,
            house_id=get_house_id(object_model.geo.address),
            offer_id=offer_id,
            price=price_in_rur,
            rooms_count=get_rooms_count(
                category=object_model.category,
                flat_type=object_model.flat_type,
                rooms_count=object_model.rooms_count
            ),
            filters=filters
        )
    )

    return entities.GetOfferValuationResponse(
        valuation_options=get_valuation_options(
            deal_type=deal_type,
            valuation_response=response,
        ),
        info_relative_market=get_info_relative_market(
            market_price=response.prices.price,
            real_price=price_in_rur,
        ),
        valuation_block_link_share=response.url,
        valuation_block_link_report=response.url,
    )
