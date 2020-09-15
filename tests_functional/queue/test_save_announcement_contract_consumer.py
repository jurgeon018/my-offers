import asyncio
from datetime import datetime, timedelta
from pathlib import Path
from copy import deepcopy
import pytest
import pytz

from tests_functional.utils import load_json_data


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ('expected_service_types'),
    (
        ['calltracking'],
        []
    )
)
async def test_process_save_announcement_correct_service_type(
    queue_service,
    pg,
    expected_service_types
):
    """
      Проверка сохранения корректного типа услуги у приходящего контракта.
    """
    # arrange
    contract = {
        'id': 1,
        'user_id': 1,
        'actor_user_id': 1,
        'publisher_user_id': 1,
        'start_date': datetime.now(pytz.utc).isoformat(),
        'payed_till': datetime.now(pytz.utc).isoformat(),
        'target_object_id': 1,
        'target_object_type': 'Announcement',
        'service_types': expected_service_types,
        'row_version': 1,
    }

    message = {
        'service_contract_reporting_model': contract,
        'operation_id': '1',
        'date': datetime.now(pytz.utc).isoformat(),
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
    """
      Проверка выдачи пустой даты payed_till в ответ на запрос объявлений, если у объявления есть только 1 контракт, в котором есть услуга calltracking.
    """
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')

    contract = {
        'id': 1,
        'user_id': 1,
        'actor_user_id': 1,
        'publisher_user_id': 1,
        'start_date': datetime.now(pytz.utc).isoformat(),
        'payed_till': datetime.now(pytz.utc).isoformat(),
        'target_object_id': 209194477,
        'target_object_type': 'Announcement',
        'service_types': ['calltracking'],
        'row_version': 1,
    }

    message = {
        'service_contract_reporting_model': contract,
        'operation_id': '1',
        'date': datetime.now(pytz.utc).isoformat(),
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
            'X-Real-UserId': 29437831
        },
        json={
            'filters': {'status_tab': 'active'},
        })

    assert response.data['offers'][0]['pageSpecificInfo']['activeInfo']['payedTill'] is None


@pytest.mark.asyncio
async def test_process_save_announcement_correct_payed_till_returned(
    pg,
    queue_service,
    http
):
    """
      Проверка выдачи корректной даты payed_till если у объявления есть контракты без calltracking.
    """
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')

    expected_date = datetime.now(pytz.utc)
    contract1 = {
        'id': 1,
        'user_id': 1,
        'actor_user_id': 1,
        'publisher_user_id': 1,
        'start_date': datetime.now(pytz.utc).isoformat(),
        'payed_till': expected_date.isoformat(),
        'target_object_id': 209194477,
        'target_object_type': 'Announcement',
        'service_types': ['FreeObject'],
        'row_version': 1,
    }

    contract2 = deepcopy(contract1)
    contract2.update({
        'service_types': ['FreeObject'],
        'payed_till': (expected_date + timedelta(days=5)).isoformat(),
        'id':2
    }
    )

    message1 = {
        'service_contract_reporting_model': contract1,
        'operation_id': '1',
        'date': datetime.now(pytz.utc).isoformat(),
    }
    message2 = deepcopy(message1)
    message2['service_contract_reporting_model'] = contract2
    message2['operation_id'] = '2'

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
            'X-Real-UserId': 29437831
        },
        json={
            'filters': {'status_tab': 'active'},
        })
    print(await pg.fetchrow('SELECT count(*) FROM offers_billing_contracts'))
    assert response.data['offers'][0]['pageSpecificInfo']['activeInfo']['payedTill'] == expected_date.isoformat()
