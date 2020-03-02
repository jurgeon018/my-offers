from datetime import datetime

import pytest
from cian_core.rabbitmq.consumer import Message
from cian_test_utils import future, v

from my_offers.entities.billing import AnnouncementBillingContract
from my_offers.enums import TargetObjectType
from my_offers.queue.consumers import mark_to_delete_announcement_contract_callback, save_announcement_contract_callback
from my_offers.queue.entities import ServiceContractMessage


pytestmark = pytest.mark.gen_test


async def test_save_announcement_contract_callback(mocker):
    # arrange
    opeartion_id = mocker.sentinel.operation_id
    offer_contract = v(AnnouncementBillingContract(
        id=1,
        user_id=555,
        actor_user_id=777,
        publisher_user_id=888,
        start_date=datetime(2020, 1, 2),
        payed_till=datetime(2020, 2, 2),
        target_object_id=999999,
        target_object_type=TargetObjectType.announcement,
        service_types=[]
    ))
    message = mocker.Mock(spec=Message)
    message.data = ServiceContractMessage(
        service_contract_reporting_model=offer_contract,
        operation_id=opeartion_id,
        date=datetime(2019, 1, 2),
    )
    save_announcement_contract_mock = mocker.patch(
        'my_offers.queue.consumers.save_announcement_contract',
        return_value=future()
    )
    new_operation_id_mock = mocker.patch('my_offers.queue.consumers.new_operation_id')
    new_operation_id_mock.return_value.__enter__.return_value = opeartion_id

    # act
    await save_announcement_contract_callback([message])

    # assert
    save_announcement_contract_mock.assert_called_with(billing_contract=offer_contract)
    new_operation_id_mock.assert_called_with(opeartion_id)


async def test_mark_to_delete_announcement_contract_callback(mocker):
    # arrange
    opeartion_id = mocker.sentinel.operation_id
    offer_contract = v(AnnouncementBillingContract(
        id=1,
        user_id=555,
        actor_user_id=777,
        publisher_user_id=888,
        start_date=datetime(2020, 1, 2),
        payed_till=datetime(2020, 2, 2),
        target_object_id=999999,
        target_object_type=TargetObjectType.announcement,
        service_types=[]
    ))
    message = mocker.Mock(spec=Message)
    message.data = ServiceContractMessage(
        service_contract_reporting_model=offer_contract,
        operation_id=opeartion_id,
        date=datetime(2019, 1, 2),
    )
    mark_to_delete_announcement_contract = mocker.patch(
        'my_offers.queue.consumers.mark_to_delete_announcement_contract',
        return_value=future()
    )
    new_operation_id_mock = mocker.patch('my_offers.queue.consumers.new_operation_id')
    new_operation_id_mock.return_value.__enter__.return_value = opeartion_id

    # act
    await mark_to_delete_announcement_contract_callback([message])

    # assert
    mark_to_delete_announcement_contract.assert_called_with(offer_contract=offer_contract)
    new_operation_id_mock.assert_called_with(opeartion_id)
