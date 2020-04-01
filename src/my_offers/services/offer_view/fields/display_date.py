from datetime import datetime
from typing import Optional

from my_offers.services.offer_view.helpers.time import get_aware_date


def get_display_date(created_at: Optional[datetime], edited_at: Optional[datetime]) -> Optional[datetime]:
    date = edited_at if edited_at else created_at

    return get_aware_date(date)
