from datetime import datetime

import pytz

from my_offers import entities
from my_offers.repositories.postgresql import save_moderation_alerts_last_visit_date


async def v1_hide_warnings_public(
        request: entities.HideWarningsRequest,
        realty_user_id: int
) -> None:
    if request.tab_type.is_declined:
        await save_moderation_alerts_last_visit_date(
            user_id=realty_user_id,
            last_visit_date=datetime.now(tz=pytz.UTC)
        )

    return None
