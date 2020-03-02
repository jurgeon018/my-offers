from datetime import datetime

import pytest
from cian_test_utils import future, v

from my_offers import pg
from my_offers.entities import AnnouncementBillingContract
from my_offers.enums import TargetObjectType
from my_offers.mappers.billing import offer_billing_contract_mapper
from my_offers.repositories import postgresql


pytestmark = pytest.mark.gen_test


async def test_save_offer_contract(mocker):
    # arrange
    is_deleted = False
    offer_contract = v(AnnouncementBillingContract(
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

    # act
    await postgresql.save_offer_contract(offer_contract=offer_contract)

    # assert
    pg.get().execute.assert_called_once_with(
        'INSERT INTO offers_billing_contracts (id, user_id, actor_user_id, publisher_user_id, target_object_id, '
        'target_object_type, start_date, payed_till, row_version, is_deleted)'
        ' VALUES ($2, $21, $1, $15, $19, $20, $18, $14, $17, $3) '
        'ON CONFLICT (id) '
        'DO UPDATE SET id = $4, user_id = $6, actor_user_id = $7, publisher_user_id = $8, target_object_id = $9, '
        'target_object_type = $10, start_date = $11, payed_till = $12, row_version = $13, is_deleted = $5 '
        'WHERE offers_billing_contracts.row_version < $16',
        offer_contract.actor_user_id,
        offer_contract.id,
        is_deleted,
        offer_contract.id,
        is_deleted,
        offer_contract.user_id,
        offer_contract.actor_user_id,
        offer_contract.publisher_user_id,
        offer_contract.target_object_id,
        offer_contract.target_object_type.name,
        offer_contract.start_date,
        offer_contract.payed_till,
        offer_contract.row_version,
        offer_contract.payed_till,
        offer_contract.publisher_user_id,
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
    pg.get().fetchrow.return_value = future(offer_contract)

    # act
    result = await postgresql.get_offer_contract(contract_id=expected_contract_id)

    # assert
    assert result == offer_billing_contract_mapper.map_from(offer_contract)
    pg.get().fetchrow.assert_called_once_with(
        'SELECT '
        'offers_billing_contracts.id, offers_billing_contracts.user_id, offers_billing_contracts.actor_user_id, '
        'offers_billing_contracts.publisher_user_id, offers_billing_contracts.target_object_id, '
        'offers_billing_contracts.target_object_type, offers_billing_contracts.start_date, '
        'offers_billing_contracts.payed_till, offers_billing_contracts.row_version, '
        'offers_billing_contracts.is_deleted '
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
        'SELECT '
        'offers_billing_contracts.id, offers_billing_contracts.user_id, offers_billing_contracts.actor_user_id, '
        'offers_billing_contracts.publisher_user_id, offers_billing_contracts.target_object_id, '
        'offers_billing_contracts.target_object_type, offers_billing_contracts.start_date, '
        'offers_billing_contracts.payed_till, offers_billing_contracts.row_version, '
        'offers_billing_contracts.is_deleted '
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
