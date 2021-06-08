from typing import Dict, Final, List, Union

from cian_entities import EntityMapper

from my_offers import enums
from my_offers.entities import get_offers, mobile_offer


get_offers_filters_mapper = EntityMapper(get_offers.Filter, without_camelcase=True)

get_offers_filters_mobile_mapper = EntityMapper(mobile_offer.Filters, without_camelcase=True)

MOBILE_TAB_TYPE_TO_STATUS_TYPE: Final[Dict[enums.MobTabTypeV1, Union[str, List[str]]]] = {
    enums.MobTabTypeV1.sale: enums.OfferStatusTab.active.value,
    enums.MobTabTypeV1.rent: enums.OfferStatusTab.active.value,
    enums.MobTabTypeV1.archived: enums.OfferStatusTab.archived.value,
    enums.MobTabTypeV1.inactive: [enums.OfferStatusTab.not_active.value, enums.OfferStatusTab.declined.value],
}

MOBILE_TAB_TYPE_TO_STATUS_TYPE_V2: Final[Dict[enums.MobTabTypeV2, str]] = {
    enums.MobTabTypeV2.sale: enums.OfferStatusTab.active.value,
    enums.MobTabTypeV2.rent: enums.OfferStatusTab.active.value,
    enums.MobTabTypeV2.archived: enums.OfferStatusTab.archived.value,
    enums.MobTabTypeV2.inactive: enums.OfferStatusTab.not_active.value,
    enums.MobTabTypeV2.declined: enums.OfferStatusTab.declined.value
}
