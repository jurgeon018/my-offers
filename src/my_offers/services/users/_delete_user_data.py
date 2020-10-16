from my_offers.repositories import postgresql


async def delete_user_data(user_id: int) -> None:
    await postgresql.add_offer_to_delete_queue_by_master_user_id(user_id)

    master_user_id = await postgresql.get_master_user_id(user_id)
    if user_id != master_user_id:
        await postgresql.add_offer_to_delete_queue_by_user_id(master_user_id=master_user_id, user_id=user_id)

    await postgresql.delete_agents_hierarchy(user_id)
