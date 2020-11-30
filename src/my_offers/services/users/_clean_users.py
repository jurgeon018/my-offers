from my_offers.repositories import postgresql
from my_offers.repositories.users import v1_get_users
from my_offers.repositories.users.entities import UserIdsRequest
from ._delete_user_data import delete_user_data


async def clean_users() -> None:
    while user_ids := await postgresql.get_user_reindex_ids():
        response = await v1_get_users(UserIdsRequest(user_ids=user_ids))
        exist_user_ids = {user.id for user in response.users}

        to_delete_user_ids = set(user_ids) - exist_user_ids
        for user_id in to_delete_user_ids:
            await delete_user_data(user_id)

        await postgresql.delete_user_reindex_items(user_ids)
