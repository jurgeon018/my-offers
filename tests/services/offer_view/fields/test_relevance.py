from datetime import datetime

import pytest
import pytz
from cian_test_utils import v

from my_offers.entities.get_offers import Relevance
from my_offers.entities.offer_relevance_warning import OfferRelevanceWarningInfo
from my_offers.services.offer_view.fields.relevance import get_relevance
from my_offers.services.offer_view import constants


@pytest.mark.parametrize('offer_relevance_warning, expected_result', (
    (None, None),
    (
        OfferRelevanceWarningInfo(
            offer_id=1,
            check_id='foo',
        ),
        Relevance(
            warning_message=constants.RELEVANCE_REGULAR_MESSAGE_TEXT,
            check_id='foo',
        ),
    ),
    (
        OfferRelevanceWarningInfo(
            offer_id=1,
            check_id='bar',
            due_date=datetime(2020, 3, 20, tzinfo=pytz.UTC),
        ),
        Relevance(
            warning_message=constants.RELEVANCE_DUE_DATE_MESSAGE_TEXT.format(
                formatted_date='20 марта 2020 года',
            ),
            check_id='bar',
        ),
    ),
))
def test_get_relevance(offer_relevance_warning, expected_result):
    # act
    result = get_relevance(offer_relevance_warning)

    # assert
    assert result == v(expected_result)
