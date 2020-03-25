from typing import List

from my_offers.helpers import category
from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel, address_info
from my_offers.services.offers.enrich.enrich_data import EnrichParams


def prepare_enrich_params(*, models: List[ObjectModel], user_id: int) -> EnrichParams:
    result = EnrichParams(user_id)

    for model in models:
        result.add_offer_id(model.id)
        offer_type, deal_type = category.get_types(model.category)

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
