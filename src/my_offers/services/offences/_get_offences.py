from typing import List, Set

from my_offers.repositories.moderation import (
    v1_get_image_offences_for_announcements,
    v1_get_video_offences_for_announcements,
)
from my_offers.repositories.moderation.entities import (
    GetImageOffencesForAnnouncementsRequest,
    GetImageOffencesForAnnouncementsResponse,
    GetVideoOffencesForAnnouncementsRequest,
    GetVideoOffencesForAnnouncementsResponse,
)


async def get_offers_with_image_offences(offers_ids: List[int]) -> Set[int]:
    image_offence: GetImageOffencesForAnnouncementsResponse = await v1_get_image_offences_for_announcements(
        GetImageOffencesForAnnouncementsRequest(announcement_ids=offers_ids)
    )

    return {i.announcement_id for i in image_offence.items}


async def get_offers_with_video_offences(offers_ids: List[int]) -> Set[int]:
    video_offence: GetVideoOffencesForAnnouncementsResponse = await v1_get_video_offences_for_announcements(
        GetVideoOffencesForAnnouncementsRequest(announcement_ids=offers_ids)
    )

    return {v.announcement_id for v in video_offence.items}
