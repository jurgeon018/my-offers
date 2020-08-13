from typing import List

from my_offers.helpers import category, fields
from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel, address_info
from my_offers.services.offers.enrich.enrich_data import EnrichParams


def prepare_enrich_params(*, models: List[ObjectModel], user_id: int) -> EnrichParams:
    result = EnrichParams(user_id=user_id)

    for model in models:
        offer_id = model.id
        result.add_offer_id(offer_id)
        offer_type, deal_type = category.get_types(model.category)

        if fields.is_test(model):
            result.add_is_test_offer(offer_id=offer_id)

        if model.published_user_id != user_id:
            result.add_agent_id(model.published_user_id)

        if geo := model.geo:
            if geo.jk and geo.jk.id:
                result.add_jk_id(geo.jk.id)

            if geo.undergrounds:
                for underground in geo.undergrounds:
                    if underground.is_default and underground.id:
                        result.add_geo_url_id(
                            geo_type=address_info.Type.underground,
                            geo_id=underground.id,
                            deal_type=deal_type,
                            offer_type=offer_type,
                        )
                        break

            if geo.address:
                for address in geo.address:
                    result.add_geo_url_id(
                        geo_type=address.type,
                        geo_id=address.id,
                        deal_type=deal_type,
                        offer_type=offer_type,
                    )

    return result
