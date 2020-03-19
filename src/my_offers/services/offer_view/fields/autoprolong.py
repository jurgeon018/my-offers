from typing import Optional

from my_offers.repositories.monolith_cian_announcementapi.entities import PublishTerms
from my_offers.services.offer_view.helpers.get_main_term import get_main_term


def is_autoprolong(publish_terms: Optional[PublishTerms]) -> bool:
    if not publish_terms:
        return False

    if not publish_terms.autoprolong:
        return False

    # не выводим автопродление если размещение с посуточной оплатой
    main_term = get_main_term(publish_terms.terms)
    if main_term and main_term.days == 1:
        return False

    return True
