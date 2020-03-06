from typing import Optional

from my_offers.entities import get_offers
from my_offers.entities.moderation import OfferOffence
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Status
from my_offers.services.offer_view.fields import get_moderation


def get_declined_info(*, status: Optional[Status], offer_offence=Optional[OfferOffence]) -> get_offers.DeclinedInfo:
    return get_offers.DeclinedInfo(
        moderation=get_moderation(
            status=status,
            offer_offence=offer_offence,
        )
    )
