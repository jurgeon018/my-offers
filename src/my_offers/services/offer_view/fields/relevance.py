from datetime import datetime
from typing import Optional

from pytils.dt import ru_strftime

from my_offers.entities.get_offers import Relevance
from my_offers.entities.offer_relevance_warning import OfferRelevanceWarning
from my_offers.services.offer_view import constants


def get_relevance(offer_relevance_warning: Optional[OfferRelevanceWarning]) -> Optional[Relevance]:
    if not offer_relevance_warning:
        return None

    return Relevance(
        warning_message=_get_warning_message(offer_relevance_warning),
        check_id=offer_relevance_warning.check_id,
    )


def _get_warning_message(offer_relevance_warning: OfferRelevanceWarning) -> Optional[str]:
    if due_date := offer_relevance_warning.due_date:
        return constants.RELEVANCE_DUE_DATE_MESSAGE_TEXT.format(formatted_date=_get_formatted_date(due_date))

    return constants.RELEVANCE_REGULAR_MESSAGE_TEXT


def _get_formatted_date(due_date: datetime) -> str:
    return ru_strftime(
        format=constants.RELEVANCE_DUE_DATE_FORMAT,
        date=due_date,
        inflected=True,
    )
