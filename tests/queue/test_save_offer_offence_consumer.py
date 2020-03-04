from datetime import datetime

import pytest
from cian_core.rabbitmq.consumer import Message
from cian_test_utils import future, v

from my_offers.entities import ModerationOfferOffence
from my_offers.enums import ModerationOffenceStatus
from my_offers.queue.consumers import save_offer_offence_callback


pytestmark = pytest.mark.gen_test


async def test_save_announcement_contract_callback(mocker):
    # arrange
    opeartion_id = '213123231'
    moderation_offer_offence = v(ModerationOfferOffence(
        offence_id=555,
        offence_type=1,
        text_for_user='ТЕСТ',
        state=ModerationOffenceStatus.confirmed,
        object_id=777,
        created_by=888,
        created_date=datetime(2020, 1, 1),
        date=datetime(2020, 1, 1),
        row_version=0,
        operation_id=opeartion_id,
    ))
    message = mocker.Mock(spec=Message)
    message.data = moderation_offer_offence
    save_offer_offence_mock = mocker.patch(
        'my_offers.queue.consumers.save_offer_offence',
        return_value=future()
    )
    new_operation_id_mock = mocker.patch('my_offers.queue.consumers.new_operation_id')
    new_operation_id_mock.return_value.__enter__.return_value = opeartion_id

    # act
    await save_offer_offence_callback([message])

    # assert
    save_offer_offence_mock.assert_called_with(offer_offence=moderation_offer_offence)
    new_operation_id_mock.assert_called_with(opeartion_id)
