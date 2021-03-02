from typing import Dict, Final, List, Union

from cian_entities import EntityMapper

from my_offers import enums
from my_offers.entities import get_offers, mobile_offer


get_offers_filters_mapper = EntityMapper(get_offers.Filter, without_camelcase=True)

get_offers_filters_mobile_mapper = EntityMapper(mobile_offer.Filters, without_camelcase=True)

MOBILE_TAB_TYPE_TO_STATUS_TYPE: Final[Dict[enums.MobTabType, Union[str, List[str]]]] = {
    enums.MobTabType.sale: enums.OfferStatusTab.active.value,
    enums.MobTabType.rent: enums.OfferStatusTab.active.value,
    enums.MobTabType.archived: enums.OfferStatusTab.archived.value,
    enums.MobTabType.inactive: [enums.OfferStatusTab.not_active.value, enums.OfferStatusTab.declined.value],
}
