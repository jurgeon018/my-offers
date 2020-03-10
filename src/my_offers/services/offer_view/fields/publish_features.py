from typing import List, Optional

from my_offers.repositories.monolith_cian_announcementapi.entities import PublishTerms
from my_offers.services.offer_view.fields.autoprolong import is_autoprolong
from my_offers.services.offer_view.helpers.get_main_term import get_main_term


def get_publish_features(publish_terms: Optional[PublishTerms]) -> List[str]:
    # TODO: https://jira.cian.tech/browse/CD-74186
    result = []

    if is_autoprolong(publish_terms):
        result.append('автопродление')

    return result
