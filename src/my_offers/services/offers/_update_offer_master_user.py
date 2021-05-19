from my_offers.queue import entities
from my_offers.repositories import postgresql


async def update_offer_master_user(message: entities.UpdateOfferMasterUserMessage) -> None:
    new_master_user_id = message.new_master_user_id
    offer_id = message.offer_id

    await postgresql.update_offer_master_user_id_by_id(
        offer_id=offer_id,
        new_master_user_id=new_master_user_id
    )
