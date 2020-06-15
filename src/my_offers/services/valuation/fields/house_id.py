from typing import Optional

from cian_web.exceptions import BrokenRulesException, Error

from my_offers.repositories.monolith_cian_announcementapi.entities import Geo


def get_house_id(
        geo: Geo
) -> Optional[int]:
    for detail in geo.address:
        if detail.type.is_house:
            return detail.id

    raise BrokenRulesException([
        Error(
            message='offer object_model does not have house in address, '
                    'valuation can not be provided without house_id',
            code='valuation_not_poossible',
            key='house_id'
        )
    ])
