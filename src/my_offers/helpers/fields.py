from datetime import datetime
from typing import Optional

from my_offers import enums
from my_offers.helpers.time import get_aware_date
from my_offers.repositories.monolith_cian_announcementapi.entities import Flags, ObjectModel
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Source


def is_archived(flags: Optional[Flags]) -> bool:
    return bool(flags and flags.is_archived)


def is_manual(source: Optional[Source]) -> bool:
    return not bool(source and source.is_upload)


def get_sort_date(*, object_model: ObjectModel, status_tab: enums.OfferStatusTab) -> Optional[datetime]:
    if status_tab.is_archived:
        result = object_model.archived_date
    elif object_model.edit_date:
        result = object_model.edit_date
    else:
        result = object_model.creation_date

    return get_aware_date(result)
