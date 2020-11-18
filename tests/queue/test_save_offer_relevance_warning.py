from datetime import datetime

import pytest
import pytz
from cian_core.rabbitmq.consumer import Message
from cian_test_utils import future, v

from my_offers.queue.consumers import save_offer_relevance_warning_callback
from my_offers.queue.entities import OfferRelevanceWarningMessage


@pytest.mark.gen_test
async def test_save_offer_relevance_warning_callback(mocker):
    # arrange
    expected = OfferRelevanceWarningMessage(
        realty_object_id=222,
        check_status_id='foo',
        guid='bar',
        relevance_type_message='baz',
        decline_date=datetime(2020, 3, 5, tzinfo=pytz.UTC),
        date=datetime(2020, 2, 25, tzinfo=pytz.UTC),
    )

    message = mocker.Mock(spec=Message)
    message.data = expected
    messages = [message]

    save_offer_relevance_warning_mock = mocker.patch(
        'my_offers.queue.consumers.save_offer_relevance_warning',
        return_value=future(),
    )

    # act
    await save_offer_relevance_warning_callback(messages)

    # assert
    save_offer_relevance_warning_mock.assert_called_once_with(v(expected))
