from typing import List, Optional

from my_offers.repositories.monolith_cian_announcementapi.entities import Photo


def get_main_photo_url(photos: Optional[List[Photo]]) -> Optional[str]:
    return photos[0].mini_url if photos else None
