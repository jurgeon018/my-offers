from attr import asdict

from my_offers.repositories.monolith_cian_announcementapi import v1_get_announcement
from my_offers.repositories.monolith_cian_announcementapi.entities import V1GetAnnouncement
from my_offers.services.announcement import process_announcement


async def update_offer(offer_id: int) -> None:
    object_model = await v1_get_announcement(V1GetAnnouncement(id=offer_id))
    await process_announcement(asdict(object_model))
