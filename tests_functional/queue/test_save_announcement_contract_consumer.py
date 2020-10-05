import asyncio
from copy import deepcopy
from datetime import datetime, timedelta
from pathlib import Path

import pytest
import pytz


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ('expected_service_types'),
    (
        [
            'FreeObject', 'DebitObject', 'PremiumObject', 'Top3',
            'Highlight', 'calltracking', 'XmlImport', 'SubscriptionForPackage',
            'StatusPro', 'ServicePackageActivation', 'Penalty', 'OrderCancellation',
            'OrderTransfer', 'TechSpend', 'TechTransfer', 'BonusPaymentExpiration',
            'auction', 'demand', 'demandPackage', 'cplCalltracking'
        ],
        []
    )
)
async def test_process_save_announcement_correct_service_type(
    queue_service,
    pg,
    expected_service_types
):
    """ Проверка сохранения корректного типа услуги у приходящего контракта.
    """
    # arrange
    now_isoformat = datetime.now(pytz.utc).isoformat()

    contract = {
        'id': 1,
        'user_id': 1,
        'actor_user_id': 1,
        'publisher_user_id': 1,
        'start_date': now_isoformat,
        'payed_till': now_isoformat,
        'target_object_id': 1,
        'target_object_type': 'Announcement',
        'service_types': expected_service_types,
        'row_version': 1,
    }

    message = {
        'service_contract_reporting_model': contract,
        'operation_id': '1',
        'date': now_isoformat,
    }
    # act
    await queue_service.wait_consumer('my-offers.save_announcement_contract')
    await queue_service.publish('service-contract-reporting.v1.created', message, exchange='billing')
    await asyncio.sleep(1)

    # assert
    row = await pg.fetchrow('SELECT * FROM offers_billing_contracts ORDER BY offer_id DESC LIMIT 1')

    assert row['service_types'] == expected_service_types


@pytest.mark.asyncio
async def test_process_save_announcement_empty_payed_till_returned_for_calltracking(
    pg,
    queue_service,
    http
):
    """ Проверка выдачи пустой даты payed_till в ответ на запрос
        объявлений, если у объявления есть только 1 контракт,
        в котором есть услуга calltracking.
    """
    # arrange
    user_id = 29437831
    now_isoformat = datetime.now(pytz.utc).isoformat()
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')

    contract = {
        'id': 1,
        'user_id': user_id,
        'actor_user_id': user_id,
        'publisher_user_id': user_id,
        'start_date': now_isoformat,
        'payed_till': now_isoformat,
        'target_object_id': 209194477,
        'target_object_type': 'Announcement',
        'service_types': ['calltracking'],
        'row_version': 1,
    }

    message = {
        'service_contract_reporting_model': contract,
        'operation_id': '1',
        'date': now_isoformat,
    }

    # act
    await queue_service.wait_consumer('my-offers.save_announcement_contract')
    await queue_service.publish('service-contract-reporting.v1.created', message, exchange='billing')

    await asyncio.sleep(1)

    # assert
    response = await http.request(
        'POST',
        '/public/v2/get-offers/',
        headers={
            'X-Real-UserId': user_id
        },
        json={
            'filters': {'status_tab': 'active'},
        })

    assert response.data['offers'][0]['pageSpecificInfo']['activeInfo']['payedTill'] is None


@pytest.mark.asyncio
async def test_process_save_announcement_correct_payed_till_returned_without_calltracking(
    pg,
    queue_service,
    http
):
    """ Проверка выдачи корректной даты payed_till, если у объявления есть контракты без calltracking.
    """
    # arrange
    user_id = 29437831
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')

    contract1_date = datetime.now(pytz.utc)
    contract1 = {
        'id': 1,
        'user_id': user_id,
        'actor_user_id': user_id,
        'publisher_user_id': user_id,
        'start_date': contract1_date.isoformat(),
        'payed_till': contract1_date.isoformat(),
        'target_object_id': 209194477,
        'target_object_type': 'Announcement',
        'service_types': ['FreeObject'],
        'row_version': 1,
    }
    message1 = {
        'service_contract_reporting_model': contract1,
        'operation_id': '1',
        'date': contract1_date.isoformat(),
    }

    contract2_date = contract1_date + timedelta(days=5)
    contract2 = deepcopy(contract1)
    contract2.update({
        'service_types': ['FreeObject'],
        'payed_till': contract2_date.isoformat(),
        'id': 2
    }
    )
    message2 = deepcopy(message1)
    message2.update({
        'service_contract_reporting_model': contract2,
        'operation_id': '2'
    })

    # act
    await queue_service.wait_consumer('my-offers.save_announcement_contract')

    await queue_service.publish('service-contract-reporting.v1.created', message1, exchange='billing')
    await queue_service.publish('service-contract-reporting.v1.created', message2, exchange='billing')
    await asyncio.sleep(2)

    # assert
    response = await http.request(
        'POST',
        '/public/v2/get-offers/',
        headers={
            'X-Real-UserId': user_id
        },
        json={
            'filters': {'status_tab': 'active'},
        })

    assert response.data['offers'][0]['pageSpecificInfo']['activeInfo']['payedTill'] == contract2_date.isoformat()


@pytest.mark.asyncio
async def test_process_save_announcement_correct_payed_till_returned_with_calltracking(
    pg,
    queue_service,
    http
):
    """ Проверка выдачи корректной даты payed_till если у объявления есть контракты c calltracking.
    """
    # arrange
    user_id = 29437831
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')

    contract1_date = datetime.now(pytz.utc)
    contract1 = {
        'id': 1,
        'user_id': user_id,
        'actor_user_id': user_id,
        'publisher_user_id': user_id,
        'start_date': contract1_date.isoformat(),
        'payed_till': contract1_date.isoformat(),
        'target_object_id': 209194477,
        'target_object_type': 'Announcement',
        'service_types': ['FreeObject'],
        'row_version': 1,
    }
    message1 = {
        'service_contract_reporting_model': contract1,
        'operation_id': '1',
        'date': contract1_date.isoformat(),
    }

    contract2_date = contract1_date + timedelta(days=5)
    contract2 = deepcopy(contract1)
    contract2.update({
        'service_types': ['FreeObject', 'calltracking'],
        'payed_till': contract2_date.isoformat(),
        'id': 2
    }
    )
    message2 = deepcopy(message1)
    message2.update({
        'service_contract_reporting_model': contract2,
        'operation_id': '2'
    })

    # act
    await queue_service.wait_consumer('my-offers.save_announcement_contract')

    await queue_service.publish('service-contract-reporting.v1.created', message1, exchange='billing')
    await queue_service.publish('service-contract-reporting.v1.created', message2, exchange='billing')

    await asyncio.sleep(2)

    # assert
    response = await http.request(
        'POST',
        '/public/v2/get-offers/',
        headers={
            'X-Real-UserId': user_id
        },
        json={
            'filters': {'status_tab': 'active'},
        })

    assert response.data['offers'][0]['pageSpecificInfo']['activeInfo']['payedTill'] == contract1_date.isoformat()
