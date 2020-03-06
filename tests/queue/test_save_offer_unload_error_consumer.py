from datetime import datetime

import pytest
from cian_core.rabbitmq.consumer import Message
from cian_test_utils import future

from my_offers.entities import OfferImportError
from my_offers.queue.consumers import save_offer_unload_error_callback
from my_offers.queue.entities import SaveUnloadError, SaveUnloadErrorMessage


@pytest.mark.gen_test
async def test_save_offer_unload_error_callback(mocker):
    # arrange
    message1 = mocker.Mock(spec=Message)
    message1.data = SaveUnloadErrorMessage(
        object_id=222,
        operation_id='zzzz',
        date=datetime(2020, 3, 5),
        error=SaveUnloadError(
            type='yyy',
            message='ffff',
        ),
    )
    message2 = mocker.Mock(spec=Message)
    message2.data = SaveUnloadErrorMessage(
        object_id=None,
        operation_id='bbb',
        date=datetime(2020, 3, 5),
        error=SaveUnloadError(
            type='ggg',
            message='nnnn',
        ),
    )
    messages = [message1, message2]

    save_offers_import_error_mock = mocker.patch(
        'my_offers.queue.consumers.save_offers_import_error',
        return_value=future()
    )

    expected = [
        OfferImportError(
            offer_id=222,
            type='yyy',
            message='ffff',
            created_at=datetime(2020, 3, 5, 0, 0)
        )
    ]

    # act
    await save_offer_unload_error_callback(messages)

    # assert
    save_offers_import_error_mock.assert_called_once_with(expected)
