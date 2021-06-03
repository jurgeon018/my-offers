from datetime import datetime

import pytz

from my_offers import entities
from my_offers.repositories.postgresql import save_last_visit_date


async def v1_hide_warnings_public(
        _: entities.MobileGetMyOffersRequest,
        realty_user_id: int
) -> None:
    await save_last_visit_date(
        user_id=realty_user_id,
        last_visit_date=datetime.now(tz=pytz.UTC)
    )

    return None
