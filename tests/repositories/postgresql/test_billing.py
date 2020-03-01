from datetime import datetime

import pytest
from cian_json import json
from cian_test_utils import future, v

from my_offers import pg
from my_offers.entities import OfferBillingContract
from my_offers.enums import TargetObjectType
from my_offers.mappers.billing import service_contract_mapper
from my_offers.repositories import postgresql


pytestmark = pytest.mark.gen_test


async def test_save_offer_contract(mocker):
    # arrange
    is_deleted = False
    offer_contract = v(OfferBillingContract(
        id=1,
        user_id=666,
        actor_user_id=777,
        publisher_user_id=888,
        start_date=datetime(2020, 1, 2),
        payed_till=datetime(2020, 2, 2),
        target_object_id=999999,
        target_object_type=TargetObjectType.announcement,
        service_types=[],
        row_version=1111111
    ))
    offer_contract_json = json.dumps(service_contract_mapper.map_to(offer_contract))

    # act
    await postgresql.save_offer_contract(offer_contract=offer_contract)

    # assert
    pg.get().execute.assert_called_once_with(
        'INSERT INTO offers_billing_contracts (id, user_id, actor_user_id, publisher_user_id, target_object_id, '
        'target_object_type, start_date, payed_till, raw_data, row_version, is_deleted) '
        'VALUES ($2, $22, $1, $15, $20, $21, $19, $14, $16, $18, $3) '
        'ON CONFLICT (id) '
        'DO UPDATE SET id = $4, user_id = $6, actor_user_id = $7, publisher_user_id = $8, target_object_id = $9, '
        'target_object_type = $10, start_date = $11, payed_till = $12, raw_data = $13, row_version = $5 '
        'WHERE offers_billing_contracts.row_version < $17',
        offer_contract.actor_user_id,
        offer_contract.id,
        is_deleted,
        offer_contract.id,
        offer_contract.row_version,
        offer_contract.user_id,
        offer_contract.actor_user_id,
        offer_contract.publisher_user_id,
        offer_contract.target_object_id,
        offer_contract.target_object_type.name,
        offer_contract.start_date,
        offer_contract.payed_till,
        offer_contract_json,
        offer_contract.payed_till,
        offer_contract.publisher_user_id,
        offer_contract_json,
        offer_contract.row_version,
        offer_contract.row_version,
        offer_contract.start_date,
        offer_contract.target_object_id,
        offer_contract.target_object_type.name,
        offer_contract.user_id,
    )


async def test_get_offer_contract(mocker):
    # arrange
    expected_contract_id = 1
    offer_contract = dict(
        id=expected_contract_id,
        user_id=666,
        actor_user_id=777,
        publisher_user_id=888,
        start_date=datetime(2020, 1, 2),
        payed_till=datetime(2020, 2, 2),
        target_object_id=999999,
        target_object_type=TargetObjectType.announcement,
        service_types=[]
    )
    pg.get().fetchrow.return_value = future({'raw_data': json.dumps(offer_contract)})

    # act
    result = await postgresql.get_offer_contract(contract_id=expected_contract_id)

    # assert
    assert result == service_contract_mapper.map_from(offer_contract)
    pg.get().fetchrow.assert_called_once_with(
        'SELECT offers_billing_contracts.raw_data '
        '\nFROM offers_billing_contracts '
        '\nWHERE offers_billing_contracts.id = $1',
        expected_contract_id
    )


async def test_get_offer_contract__contract_is_none(mocker):
    # arrange
    expected_contract_id = 1
    pg.get().fetchrow.return_value = future([])

    # act
    result = await postgresql.get_offer_contract(contract_id=expected_contract_id)

    # assert
    assert result is None
    pg.get().fetchrow.assert_called_once_with(
        'SELECT offers_billing_contracts.raw_data '
        '\nFROM offers_billing_contracts '
        '\nWHERE offers_billing_contracts.id = $1',
        expected_contract_id
    )


async def test_set_offer_contract_is_deleted_status(mocker):
    # arrange
    contract_id = 666
    row_version = 1231212
    is_deleted = True

    # act
    await postgresql.set_offer_contract_is_deleted_status(
        contract_id=contract_id,
        row_version=row_version
    )

    # assert
    pg.get().execute.assert_called_once_with(
        'UPDATE offers_billing_contracts '
        'SET is_deleted=$2 '
        'WHERE offers_billing_contracts.row_version < $3 '
        'AND offers_billing_contracts.id = $1',
        contract_id,
        is_deleted,
        row_version,
    )
