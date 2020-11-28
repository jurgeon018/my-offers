from my_offers.repositories.postgresql.user_reindex_queue import delete_reindex_items, get_reindex_items
from my_offers.repositories.users import v1_get_users
from my_offers.repositories.users.entities import UserIdsRequest
from my_offers.services.users import delete_user_data


async def clean_users() -> None:
    while user_ids := await get_reindex_items():
        users = await v1_get_users(UserIdsRequest(user_ids=user_ids))
        exist_user_ids = {user.id for user in users}

        to_delete_user_ids = set(user_ids) - exist_user_ids
        for user_id in to_delete_user_ids:
            await delete_user_data(user_id)

        await delete_reindex_items(user_ids)
