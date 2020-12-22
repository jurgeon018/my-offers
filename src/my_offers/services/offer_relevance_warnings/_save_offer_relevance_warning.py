from datetime import datetime
from typing import Optional

from my_offers import pg
from my_offers.entities.offer_relevance_warning import OfferRelevanceWarning
from my_offers.queue.entities import OfferRelevanceWarningMessage
from my_offers.queue.enums import OfferRelevanceCheckStatusId, OfferRelevanceTypeMessage
from my_offers.repositories import postgresql


async def save_offer_relevance_warning(offer_relevance_warning: OfferRelevanceWarningMessage) -> None:
    offer_id = offer_relevance_warning.realty_object_id
    active = map_active(offer_relevance_warning)
    async with pg.get().transaction():
        await postgresql.update_offer_has_active_relevance_warning(
            offer_id=offer_id,
            has_active_relevance_warning=active,
        )
        await postgresql.save_offer_relevance_warning(OfferRelevanceWarning(
            offer_id=offer_id,
            check_id=offer_relevance_warning.guid,
            created_at=offer_relevance_warning.date,
            updated_at=offer_relevance_warning.date,
            due_date=map_due_date(offer_relevance_warning),
            active=active,
        ))


def map_active(offer_relevance_warning_message: OfferRelevanceWarningMessage) -> bool:
    if offer_relevance_warning_message.relevance_type_message == OfferRelevanceTypeMessage.without_message.value:
        return False
    relevance_confirmation_required_value = OfferRelevanceCheckStatusId.relevance_confirmation_required.value
    return offer_relevance_warning_message.check_status_id == relevance_confirmation_required_value


def map_due_date(offer_relevance_warning_message: OfferRelevanceWarningMessage) -> Optional[datetime]:
    if offer_relevance_warning_message.relevance_type_message != OfferRelevanceTypeMessage.warning_only.value:
        return offer_relevance_warning_message.decline_date
    return None
