from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from my_offers import enums
from my_offers.entities.enrich import AddressUrlParams
from my_offers.repositories.monolith_cian_announcementapi.entities import address_info


class EnrichParams:
    def __init__(self) -> None:
        self._offer_ids: Dict[int, int] = {}
        self._jk_ids: Dict[int, int] = {}
        self._geo_url_params: Dict[tuple, Dict] = defaultdict(dict)

        super().__init__()

    def add_offer_id(self, offer_id: int) -> None:
        self._offer_ids[offer_id] = offer_id

    def get_offer_ids(self) -> List[int]:
        return list(self._offer_ids.keys())

    def add_jk_id(self, jk_id: int) -> None:
        self._jk_ids[jk_id] = jk_id

    def get_jk_ids(self) -> List[int]:
        return list(self._jk_ids.keys())

    def add_geo_url_id(
            self,
            *,
            deal_type: enums.DealType,
            offer_type: enums.OfferType,
            geo_type: address_info.Type,
            geo_id: int
    ) -> None:
        key = (deal_type, offer_type)
        if geo_type not in self._geo_url_params[key]:
            self._geo_url_params[key][geo_type] = {}

        self._geo_url_params[key][geo_type][geo_id] = geo_id

    def get_geo_url_params(self) -> List[AddressUrlParams]:
        result = []
        for key, values in self._geo_url_params.items():
            address = []
            for address_type, geo_ids in values.items():
                for geo_id in geo_ids:
                    address.append(address_info.AddressInfo(type=address_type, id=geo_id))

            result.append(
                AddressUrlParams(
                    deal_type=key[0],
                    offer_type=key[1],
                    address_info=address,
                )
            )

        return result

class AddressUrls:
    def __init__(self) -> None:
        self._storage: Dict[address_info.Type, Dict] = defaultdict(dict)
        super().__init__()

    def add_url(self, *, address: address_info.AddressInfo, url: str) -> None:
        self._storage[address.type][address.id] = url

    def get_url(self, address: address_info.AddressInfo) -> Optional[str]:
        if address.type not in self._storage:
            return None

        return self._storage[address.type].get(address.id)


@dataclass
class EnrichData:
    statistics: Dict[int, Any]
    auctions: Dict[int, Any]
    jk_urls: Dict[int, str]
    geo_urls: Dict[tuple, AddressUrls]

    def get_urls_by_types(
            self,
            *,
            deal_type: enums.DealType,
            offer_type: enums.OfferType
    ) -> AddressUrls:
        return self.geo_urls.get((deal_type, offer_type), AddressUrls())
