from datetime import datetime
from typing import Optional

from my_offers import enums
from my_offers.mappers.date_time import date_time_time_zone_mapper
from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel


def get_sort_date(*, object_model: ObjectModel, status_tab: enums.OfferStatusTab) -> Optional[datetime]:
    if status_tab.is_archived:
        result = object_model.archived_date
    else:
        result = object_model.edit_date

    return date_time_time_zone_mapper.map_from(result) if result else None
