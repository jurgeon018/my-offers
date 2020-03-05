from datetime import datetime

import pytz

from my_offers.entities import ModerationOfferOffence
from my_offers.entities.moderation import OfferOffence
from my_offers.repositories import postgresql


async def save_offer_offence(offer_offence: ModerationOfferOffence) -> None:
    """ Сохранить нарушение по объявлению """
    if offer_offence.row_version is None:
        # TODO: https://jira.cian.tech/browse/CD-75712
        offer_offence.row_version = 0

    now = datetime.now(pytz.utc)
    offer_offence = OfferOffence(
        offence_id=offer_offence.offence_id,
        offence_type=offer_offence.offence_type,
        offence_text=offer_offence.text_for_user,
        offence_status=offer_offence.state,
        offer_id=offer_offence.object_id,
        created_by=offer_offence.created_by,
        created_date=offer_offence.created_date,
        row_version=offer_offence.row_version,
        updated_at=now,
        created_at=now,
    )
    await postgresql.save_offer_offence(offer_offence=offer_offence)
