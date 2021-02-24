from typing import List

from my_offers.repositories.moderation_checks_orchestrator import v1_check_users_need_identification
from my_offers.repositories.moderation_checks_orchestrator.entities import (
    CheckUsersNeedIdentificationRequest,
    UserIdentificationResult,
)


async def _get_unidentified_offers(user_id: int) -> List[int]:
    result: List[UserIdentificationResult] = await v1_check_users_need_identification(
        CheckUsersNeedIdentificationRequest(
            user_ids=[user_id]
        )
    )

    for r in result:
        if r.user_id == user_id:
            return r.object_ids

    return []
