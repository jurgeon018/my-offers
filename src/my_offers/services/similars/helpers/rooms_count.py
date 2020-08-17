from typing import Optional

from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import FlatType


def get_rooms_count(
        *,
        rooms_count: Optional[int],
        rooms_for_sale_count: Optional[int],
        flat_type: Optional[FlatType],
) -> Optional[int]:
    if rooms_count:
        return rooms_count

    if rooms_for_sale_count:
        return rooms_for_sale_count

    if flat_type:
        if flat_type.is_studio:
            return 1
        if flat_type.is_open_plan:
            return 1

    return None
