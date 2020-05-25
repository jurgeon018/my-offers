from typing import List, Optional

from my_offers.repositories.monolith_cian_announcementapi.entities import Photo


def get_main_photo_url(
        photos: Optional[List[Photo]],
        better_quality: bool = False
) -> Optional[str]:
    if not photos:
        return None
    return photos[0].thumbnail_url if better_quality else photos[0].mini_url
