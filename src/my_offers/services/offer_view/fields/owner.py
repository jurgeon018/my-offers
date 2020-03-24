from typing import Optional


def is_owner(*, user_id: int, owner_id: Optional[int]) -> bool:
    if not owner_id:
        return True

    return user_id == owner_id
