from typing import List

from my_offers.services.offers.enrich.enrich import EnrichParams
from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel, address_info


def _prepare_enrich_params(models: List[ObjectModel]) -> EnrichParams:
    result = EnrichParams()

    for model in models:
        result.offer_ids.append(model.id)

        if geo := model.geo:
            if geo.jk and geo.jk.id:
                result.jk_ids.append(geo.jk.id)

            if geo.undergrounds:
                for underground in geo.undergrounds:
                    if underground.is_default and underground.id:
                        result.geo_params[address_info.Type.underground].append(underground.id)
                        break

            if geo.address:
                for address in geo.address:
                    result.geo_params[address.type].append(address.id)

    return result
