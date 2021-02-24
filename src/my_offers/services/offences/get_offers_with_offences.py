import asyncio
from typing import List, Tuple

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


async def get_offers_with_media_offences(offers_ids: List[int]) -> Tuple[List[int], List[int]]:
    image_offence: GetImageOffencesForAnnouncementsResponse
    video_offence: GetVideoOffencesForAnnouncementsResponse

    image_offence, video_offence = await asyncio.gather(
        v1_get_image_offences_for_announcements(
            GetImageOffencesForAnnouncementsRequest(
                announcement_ids=offers_ids,
            )),
        v1_get_video_offences_for_announcements(
            GetVideoOffencesForAnnouncementsRequest(
                announcement_ids=offers_ids,
            )
        )
    )

    return [i.announcement_id for i in image_offence.items], [v.announcement_id for v in video_offence.items]
