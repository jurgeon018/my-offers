from datetime import datetime
from typing import List, Optional

from my_offers import enums
from my_offers.helpers.time import get_aware_date
from my_offers.repositories.monolith_cian_announcementapi.entities import Flags, Geo, ObjectModel, Photo
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Source, Status


def is_test(object_model: ObjectModel) -> bool:
    return (
        object_model.platform
        and object_model.platform.type
        and object_model.platform.type.is_qa_autotests
    )


def is_archived(flags: Optional[Flags]) -> bool:
    return bool(flags and flags.is_archived)


def is_manual(source: Optional[Source]) -> bool:
    return not bool(source and source.is_upload)


def is_draft(status: Optional[Status]) -> bool:
    return bool(status and status.is_draft)


def get_sort_date(*, object_model: ObjectModel, status_tab: enums.OfferStatusTab) -> Optional[datetime]:
    if status_tab.is_archived:
        result = object_model.archived_date
    elif object_model.edit_date:
        result = object_model.edit_date
    else:
        result = object_model.creation_date

    return get_aware_date(result)


def get_main_photo_url(
        photos: Optional[List[Photo]],
        better_quality: bool = False
) -> Optional[str]:
    if not photos:
        return None

    for photo in photos:
        if photo.is_default:
            break
    else:
        photo = photos[0]

    if better_quality and photo.thumbnail_url:
        return photo.thumbnail_url

    return photo.mini_url


def get_locations(geo: Optional[Geo]) -> List[int]:
    if geo and geo.location_path and geo.location_path.child_to_parent:
        return geo.location_path.child_to_parent

    return []


def get_offer_payed_by(
        master_user_id: Optional[int],
        user_id: Optional[int],
        payed_by: Optional[int]
) -> Optional[enums.OfferPayedByType]:
    if not payed_by:
        return None
    if master_user_id == payed_by:
        return enums.OfferPayedByType.by_master
    if user_id == payed_by:
        return enums.OfferPayedByType.by_agent

    return None
