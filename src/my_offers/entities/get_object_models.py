from dataclasses import dataclass
from typing import List

from my_offers.entities.get_offers import PageInfo, Statistics
from my_offers.repositories.monolith_cian_announcementapi import entities as announcementapi_entities


@dataclass
class GetObjectModelsResponse:
    offers: List[announcementapi_entities.ObjectModel]
    statistics: List[Statistics]
    page: PageInfo
