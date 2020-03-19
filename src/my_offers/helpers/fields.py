from typing import Optional

from my_offers.repositories.monolith_cian_announcementapi.entities import Flags


def is_archived(flags: Optional[Flags]) -> bool:
    return bool(flags and flags.is_archived)
