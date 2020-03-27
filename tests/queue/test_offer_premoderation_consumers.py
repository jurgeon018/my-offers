from datetime import datetime

import pytest
from cian_core.rabbitmq.consumer import Message
from cian_test_utils import future

from my_offers.entities.moderation import OfferPremoderation
from my_offers.queue.consumers import remove_offer_premoderation_callback, save_offer_premoderation_callback
from my_offers.queue.entities import AnnouncementPremoderationReportingMessage


@pytest.mark.gen_test
async def test_save_offer_premoderation_callback(mocker):
    # arrange
    message = mocker.Mock(spec=Message)
    message.data = AnnouncementPremoderationReportingMessage(
        object_id=111,
        operation_id='zzzz',
        date=datetime(2020, 3, 27),
        row_version=1,
    )
    save_offer_premoderation_mock = mocker.patch(
        'my_offers.queue.consumers.save_offer_premoderation',
        return_value=future()
    )

    # act
    await save_offer_premoderation_callback([message])

    # assert
    save_offer_premoderation_mock.assert_called_once_with(
        OfferPremoderation(
            offer_id=111,
            removed=False,
            row_version=1,
        )
    )


@pytest.mark.gen_test
async def test_remove_offer_premoderation_callback(mocker):
    # arrange
    message = mocker.Mock(spec=Message)
    message.data = AnnouncementPremoderationReportingMessage(
        object_id=111,
        operation_id='zzzz',
        date=datetime(2020, 3, 27),
        row_version=1,
    )
    save_offer_premoderation_mock = mocker.patch(
        'my_offers.queue.consumers.save_offer_premoderation',
        return_value=future()
    )

    # act
    await remove_offer_premoderation_callback([message])

    # assert
    save_offer_premoderation_mock.assert_called_once_with(
        OfferPremoderation(
            offer_id=111,
            removed=True,
            row_version=1,
        )
    )
