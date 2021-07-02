from datetime import datetime
from typing import Optional

from my_offers.repositories.monolith_cian_announcementapi.entities import PublishTerms


def get_expiration_date(publish_terms: Optional[PublishTerms]) -> Optional[datetime]:
    if publish_terms is not None:
        return publish_terms.expiration_date

    return None
