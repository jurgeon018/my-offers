from datetime import datetime
from typing import Any, Dict, Optional

import pytz
from cian_core.runtime_settings import runtime_settings

from my_offers import entities
from my_offers.repositories.postgresql import get_declined_count_after_last_visit_date, get_last_visit_date
from my_offers.services.offers import get_user_filter


async def v1_has_unread_warnings_private(
        request: entities.HasUnreadWarningsRequest,
) -> entities.HasUnreadWarningsResponse:
    filters: Dict[str, Any] = await get_user_filter(request.user_id)

    last_visit_date_from_db: Optional[datetime] = await get_last_visit_date(user_id=request.user_id)

    last_visit_date: datetime = last_visit_date_from_db or datetime.utcfromtimestamp(
        runtime_settings.get('DEFAULT_LAST_VISIT_DATE', 0)
    ).replace(tzinfo=pytz.utc)

    declined_count: Optional[int] = await get_declined_count_after_last_visit_date(
        last_visit_date=last_visit_date or datetime.now(tz=pytz.UTC),
        filters=filters,
    )

    return entities.HasUnreadWarningsResponse(has_warnings=bool(declined_count))
