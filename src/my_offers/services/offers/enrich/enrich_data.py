from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, List, NamedTuple, Optional, Set

from simple_settings import settings

from my_offers import enums
from my_offers.entities import AgentHierarchyData
from my_offers.entities.enrich import AddressUrlParams
from my_offers.entities.mobile_offer import OfferAuction, OfferComplaint, OfferDeactivatedService
from my_offers.entities.moderation import OfferOffence
from my_offers.entities.offer_relevance_warning import OfferRelevanceWarning
from my_offers.entities.offer_view_model import Subagent
from my_offers.enums import DuplicateTabType, OfferPayedByType
from my_offers.repositories.agencies_settings.entities import AgencySettings
from my_offers.repositories.callbook.entities import OfferCallCount
from my_offers.repositories.monolith_cian_announcementapi.entities import address_info


class GeoUrlKey(NamedTuple):
    deal_type: enums.DealType
    offer_type: enums.OfferType


class EnrichParams:

    def __init__(self, user_id: int, is_test_offers: bool = False) -> None:
        self._offer_ids: Set[int] = set()
        self._jk_ids: Set[int] = set()
        self._agent_ids: Set[int] = set()
        self._geo_url_params: Dict[GeoUrlKey, Dict] = defaultdict(dict)
        self._user_id = user_id
        self._similar_offers: Set[int] = set()

        self.is_test_offers: bool = is_test_offers

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

    def add_similar_offer(self, offer_id: int) -> None:
        self._similar_offers.add(offer_id)

    def get_similar_offers(self) -> List[int]:
        return list(self._similar_offers)


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
class BaseEnrichData:
    agent_hierarchy_data: AgentHierarchyData
    agency_settings: Optional[AgencySettings] = None
    offers_payed_by: Dict[int, Optional[OfferPayedByType]] = field(default_factory=dict)
    can_update_edit_dates: Dict[int, bool] = field(default_factory=dict)
    payed_till: Optional[Dict[int, datetime]] = None
    archive_date: Optional[Dict[int, datetime]] = None
    # statistics
    views_counts: Dict[int, int] = field(default_factory=dict)
    searches_counts: Dict[int, int] = field(default_factory=dict)
    favorites_counts: Dict[int, int] = field(default_factory=dict)
    offers_similars_counts: Dict[DuplicateTabType, Dict[int, int]] = field(default_factory=dict)
    calls_count: Dict[int, OfferCallCount] = field(default_factory=dict)

    def get_payed_till(self, offer_id: int) -> Optional[datetime]:
        if not self.payed_till:
            return None

        return self.payed_till.get(offer_id)

    def get_duplicates_counts(self, offer_id: int) -> Optional[int]:
        return self.offers_similars_counts.get(DuplicateTabType.duplicate, {}).get(offer_id)

    def get_same_building_counts(self, offer_id: int) -> Optional[int]:
        return self.offers_similars_counts.get(DuplicateTabType.same_building, {}).get(offer_id)

    def get_archive_date(self, offer_id: int) -> Optional[datetime]:
        if not self.archive_date:
            return None

        updated_at = self.archive_date.get(offer_id)
        if not updated_at:
            return None

        return updated_at + timedelta(days=settings.DAYS_BEFORE_ARCHIVATION)

    def get_calls_count(self, offer_id: int) -> Optional[int]:
        if offer_id not in self.calls_count:
            return None

        return self.calls_count[offer_id].calls_count

    def get_missed_calls_count(self, offer_id: int) -> Optional[int]:
        if offer_id not in self.calls_count:
            return None

        return self.calls_count[offer_id].missed_calls_count


@dataclass
class EnrichData(BaseEnrichData):
    auctions: Dict[int, Any] = field(default_factory=dict)
    jk_urls: Dict[int, str] = field(default_factory=dict)
    geo_urls: Dict[GeoUrlKey, AddressUrls] = field(default_factory=dict)
    import_errors: Dict[int, str] = field(default_factory=dict)
    moderation_info: Optional[Dict[int, OfferOffence]] = None
    subagents: Optional[Dict[int, Subagent]] = None
    premoderation_info: Optional[Set[int]] = None
    offer_relevance_warnings: Optional[Dict[int, OfferRelevanceWarning]] = None

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

    def get_offer_relevance_warning(self, offer_id: int) -> Optional[OfferRelevanceWarning]:
        if not self.offer_relevance_warnings:
            return None

        return self.offer_relevance_warnings.get(offer_id)


@dataclass
class MobileEnrichData(BaseEnrichData):
    video_offences: Set[int] = field(default_factory=set)
    image_offences: Set[int] = field(default_factory=set)
    moderation_info: Optional[Dict[int, List[OfferComplaint]]] = field(default=None)
    premoderation_info: Optional[Set[int]] = field(default=None)
    offer_with_pending_identification: Set[int] = field(default_factory=set)
    auctions: Dict[int, OfferAuction] = field(default_factory=dict)
    views_daily_counts: Dict[int, int] = field(default_factory=dict)
    deactivated_service: Dict[int, OfferDeactivatedService] = field(default_factory=dict)


    def get_offer_offence(self, offer_id: int) -> Optional[List[OfferComplaint]]:
        if not self.moderation_info:
            return None

        return self.moderation_info.get(offer_id)

    def get_offer_auction(self, offer_id: int) -> Optional[OfferAuction]:
        if not self.auctions:
            return None

        return self.auctions.get(offer_id)

    def on_premoderation(self, offer_id) -> bool:
        if not self.premoderation_info:
            return False

        return offer_id in self.premoderation_info

    def wait_identification(self, offer_id) -> bool:
        if not self.offer_with_pending_identification:
            return False

        return offer_id in self.offer_with_pending_identification

    def get_deactivated_service(self, offer_id: int) -> Optional[OfferDeactivatedService]:
        if offer_id not in self.deactivated_service:
            return None

        return self.deactivated_service[offer_id]
