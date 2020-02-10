from my_offers import entities
from my_offers.mappers.object_model import object_model_mapper
from my_offers.repositories.monolith_cian_announcementapi import v1_get_announcement
from my_offers.repositories.monolith_cian_announcementapi.entities import V1GetAnnouncement
from my_offers.services.announcement import process_announcement


async def update_offer(request: entities.UpdateOfferRequest) -> None:
    object_model = await v1_get_announcement(V1GetAnnouncement(id=request.offer_id))
    await process_announcement(object_model_mapper.map_to(object_model))
