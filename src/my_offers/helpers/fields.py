from typing import Optional

from my_offers.repositories.monolith_cian_announcementapi.entities import Flags
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Source


def is_archived(flags: Optional[Flags]) -> bool:
    return bool(flags and flags.is_archived)


def is_xml_import(source: Optional[Source]) -> bool:
    return not bool(source and source.is_upload)
