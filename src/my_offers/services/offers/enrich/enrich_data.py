from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, List, NamedTuple, Optional, Set

from simple_settings import settings

from my_offers import enums
from my_offers.entities.enrich import AddressUrlParams
from my_offers.entities.moderation import OfferOffence
from my_offers.entities.offer_view_model import Subagent
from my_offers.repositories.agencies_settings.entities import AgencySettings
from my_offers.repositories.monolith_cian_announcementapi.entities import address_info


class GeoUrlKey(NamedTuple):
    deal_type: enums.DealType
    offer_type: enums.OfferType


class EnrichParams:

    def __init__(self, user_id: int) -> None:
        self._offer_ids: Set[int] = set()
        self._jk_ids: Set[int] = set()
        self._agent_ids: Set[int] = set()
        self._geo_url_params: Dict[GeoUrlKey, Dict] = defaultdict(dict)
        self._user_id = user_id

    def get_user_id(self):
        return self._user_id

    def add_offer_id(self, offer_id: int) -> None:
        self._offer_ids.add(offer_id)

    def get_offer_ids(self) -> List[int]:
        return list(self._offer_ids)

    def add_agent_id(self, user_id: int) -> None:
        self._agent_ids.add(user_id)

    def get_agent_ids(self) -> List[int]:
        return list(self._agent_ids)

    def add_jk_id(self, jk_id: int) -> None:
        self._jk_ids.add(jk_id)

    def get_jk_ids(self) -> List[int]:
        return list(self._jk_ids)

    def add_geo_url_id(
            self,
            *,
            deal_type: enums.DealType,
            offer_type: enums.OfferType,
            geo_type: address_info.Type,
            geo_id: int
    ) -> None:
        key = GeoUrlKey(deal_type, offer_type)
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

    def add_url(self, *, address: address_info.AddressInfo, url: str) -> None:
        self._storage[address.type][address.id] = url

    def get_url(self, address: address_info.AddressInfo) -> Optional[str]:
        if address.type not in self._storage:
            return None

        return self._storage[address.type].get(address.id)


class EnrichItem(NamedTuple):
    key: str
    value: Any
    degraded: bool


@dataclass
class EnrichData:
    auctions: Dict[int, Any] = field(default_factory=dict)
    jk_urls: Dict[int, str] = field(default_factory=dict)
    geo_urls: Dict[GeoUrlKey, AddressUrls] = field(default_factory=dict)
    can_update_edit_dates: Dict[int, bool] = field(default_factory=dict)
    import_errors: Dict[int, str] = field(default_factory=dict)
    moderation_info: Optional[Dict[int, OfferOffence]] = None
    agency_settings: Optional[AgencySettings] = None
    subagents: Optional[Dict[int, Subagent]] = None
    premoderation_info: Optional[Set[int]] = None
    archive_date: Optional[Dict[int, datetime]] = None
    payed_till: Optional[Dict[int, datetime]] = None
    allow_change_publisher: Dict[int, bool] = field(default_factory=dict)

    # statistics
    views_counts: Dict[int, int] = field(default_factory=dict)
    searches_counts: Dict[int, int] = field(default_factory=dict)
    favorites_counts: Dict[int, int] = field(default_factory=dict)

    def get_urls_by_types(
            self,
            *,
            deal_type: enums.DealType,
            offer_type: enums.OfferType
    ) -> AddressUrls:
        return self.geo_urls.get(GeoUrlKey(deal_type, offer_type), AddressUrls())

    def get_offer_offence(self, offer_id: int) -> Optional[OfferOffence]:
        if not self.moderation_info:
            return None

        return self.moderation_info.get(offer_id)

    def get_subagent(self, user_id) -> Optional[Subagent]:
        if not self.subagents:
            return None

        return self.subagents.get(user_id)

    def on_premoderation(self, offer_id) -> bool:
        if not self.premoderation_info:
            return False

        return offer_id in self.premoderation_info

    def get_archive_date(self, offer_id: int) -> Optional[datetime]:
        if not self.archive_date:
            return None

        updated_at = self.archive_date.get(offer_id)
        if not updated_at:
            return None

        return updated_at + timedelta(days=settings.DAYS_BEFORE_ARCHIVATION)

    def get_payed_till(self, offer_id: int) -> Optional[datetime]:
        if not self.payed_till:
            return None

        return self.payed_till.get(offer_id)
