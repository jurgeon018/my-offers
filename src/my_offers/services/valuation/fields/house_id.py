from typing import List, Optional

from cian_web.exceptions import BrokenRulesException, Error

from my_offers.repositories.monolith_cian_announcementapi.entities import AddressInfo


def get_house_id(
        address: List[AddressInfo]
) -> Optional[int]:
    for detail in address:
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
