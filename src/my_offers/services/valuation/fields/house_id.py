from typing import List, Optional

from cian_web.exceptions import BrokenRulesException, Error

from my_offers.repositories.monolith_cian_announcementapi.entities import AddressInfo
from my_offers.repositories.monolith_cian_announcementapi.entities.address_info import Type


def get_house_id(
        address: List[AddressInfo]
) -> Optional[int]:
    for detail in address:
        if detail.type == Type.house:
            return detail.id
    raise BrokenRulesException([
        Error(
            message='offer object_model does not have house in address, '
                    'valuation can not be provided without house_id',
            code='broken',
            key='house_id'
        )
    ])
