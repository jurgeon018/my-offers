from collections import defaultdict

from typing import List

from my_offers.repositories.monolith_cian_announcementapi.entities import address_info


class EnrichParams:
    def __init__(self) -> None:
        self._offer_ids = {}
        self._jk_ids = {}
        self._geo_params = defaultdict(dict)

        super().__init__()

    def add_offer_id(self, offer_id: int) -> None:
        self._offer_ids[offer_id] = offer_id

    def get_offer_ids(self) -> List[int]:
        return list(self._offer_ids.keys())

    def add_jk_id(self, jk_id: int) -> None:
        self._jk_ids[jk_id] = jk_id

    def get_jk_ids(self) -> List[int]:
        return list(self._jk_ids.keys())

    def add_geo_id(self, geo_type: address_info.Type, geo_id: int) -> None:
        self._geo_params[geo_type][geo_id] = geo_id

    def get_geo_params(self):
        return self._geo_params
