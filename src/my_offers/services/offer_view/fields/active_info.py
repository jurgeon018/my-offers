from datetime import datetime, timedelta
from typing import Optional

import pytz

from my_offers.entities import get_offers
from my_offers.repositories.monolith_cian_announcementapi.entities import PublishTerms
from my_offers.services.offer_view.fields.from_package import is_from_package
from my_offers.services.offer_view.fields.publish_features import get_publish_features
from my_offers.services.offer_view.fields.vas import get_vas


def get_active_info(publish_terms: Optional[PublishTerms], payed_till: Optional[datetime]) -> get_offers.ActiveInfo:
    terms = publish_terms.terms if publish_terms else None
    payed_remain = _get_payed_remain(payed_till)

    is_autoprolong = bool(publish_terms and publish_terms.autoprolong)
    is_publication_time_ends = bool(payed_remain and payed_remain.days < 1)

    return get_offers.ActiveInfo(
        publish_features=get_publish_features(
            publish_terms=publish_terms,
            payed_remain=payed_remain
        ),
        vas=get_vas(terms),
        is_from_package=is_from_package(terms),
        is_publication_time_ends=is_publication_time_ends and not is_autoprolong,
        payed_till=payed_till,
    )


def _get_payed_remain(payed_till: Optional[datetime]) -> Optional[timedelta]:
    if not payed_till:
        return None

    now = datetime.now(tz=pytz.UTC)
    delta = payed_till - now

    return delta
