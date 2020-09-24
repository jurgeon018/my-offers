from datetime import datetime

import pytest
from cian_test_utils import future
from simple_settings.utils import settings_stub

from my_offers import pg
from my_offers.entities import OfferBillingContract
from my_offers.mappers.billing import offer_billing_contract_mapper
from my_offers.repositories import postgresql
from my_offers.repositories.postgresql.billing import (
    get_offers_payed_till,
    get_offers_payed_till_excluding_calltracking,
)


pytestmark = pytest.mark.gen_test


async def test_save_offer_contract(mocker):
    # arrange
    now = datetime(2020, 12, 12)
    offer_contract = OfferBillingContract(
        id=1,
        user_id=555,
        actor_user_id=777,
        publisher_user_id=888,
        start_date=datetime(2020, 1, 2),
        payed_till=datetime(2020, 2, 2),
        offer_id=999999,
        row_version=0,
        is_deleted=False,
        created_at=now,
        updated_at=now,
        service_types=[],
    )
    pg.get().fetchrow.return_value = future({'id': 1})

    # act
    await postgresql.save_offer_contract(offer_contract=offer_contract)

    # assert
    pg.get().fetchrow.assert_called_once_with(
        'INSERT INTO offers_billing_contracts (id, user_id, actor_user_id, publisher_user_id, '
        'offer_id, start_date, payed_till, row_version, is_deleted, created_at, updated_at, '
        'service_types) VALUES ($3, $24, $1, $18, $5, $22, $17, $20, $4, $2, $23, CAST($21 '
        'AS offer_billing_service_type[])) ON CONFLICT (id) DO UPDATE SET id = $6, user_id '
        '= $9, actor_user_id = $10, publisher_user_id = $11, offer_id = $12, start_date = '
        '$13, payed_till = $14, row_version = $15, is_deleted = $16, updated_at = $7, '
        'service_types = CAST($8 AS offer_billing_service_type[]) WHERE offers_billing'
        '_contracts.row_version < $19 RETURNING offers_billing_contracts.id',
        offer_contract.actor_user_id,
        now,
        offer_contract.id,
        offer_contract.is_deleted,
        offer_contract.offer_id,
        offer_contract.id,
        now,
        offer_contract.service_types,
        offer_contract.user_id,
        offer_contract.actor_user_id,
        offer_contract.publisher_user_id,
        offer_contract.offer_id,
        offer_contract.start_date,
        offer_contract.payed_till,
        offer_contract.row_version,
        offer_contract.is_deleted,
        offer_contract.payed_till,
        offer_contract.publisher_user_id,
        offer_contract.row_version,
        offer_contract.row_version,
        offer_contract.service_types,
        offer_contract.start_date,
        now,
        offer_contract.user_id
    )


async def test_set_offer_contract_is_deleted_status(mocker):
    # arrange
    contract_id = 555
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


@pytest.mark.gen_test
async def test_get_offers_payed_till(mocker):
    # arrange
    pg.get().fetch.return_value = future([{'offer_id': 1, 'payed_till': datetime(2020, 3, 30)}])

    expected = {1: datetime(2020, 3, 30)}

    # act
    with settings_stub(DB_TIMEOUT=3):
        result = await get_offers_payed_till([1, 2])

    # assert
    assert result == expected
    pg.get().fetch.assert_called_once_with(
        'SELECT offers_billing_contracts.offer_id, max(offers_billing_contracts.payed_till) AS payed_till '
        '\nFROM offers_billing_contracts \nWHERE NOT offers_billing_contracts.is_deleted '
        'AND offers_billing_contracts.offer_id = ANY ($1) GROUP BY offers_billing_contracts.offer_id',
        [1, 2],
        timeout=3
    )


async def test_get_offers_payed_till_excluding_calltracking(mocker):
    # arrange
    pg.get().fetch.return_value = future([{'offer_id': 1, 'payed_till': datetime(2020, 3, 30)}])

    expected = {1: datetime(2020, 3, 30)}

    # act
    with settings_stub(DB_TIMEOUT=3):
        result = await get_offers_payed_till_excluding_calltracking([1, 2])

    # assert
    assert result == expected
    pg.get().fetch.assert_called_once_with(
        'SELECT offers_billing_contracts.offer_id, max(offers_billing_contracts.payed_till) AS payed_till '
        '\nFROM offers_billing_contracts \nWHERE NOT offers_billing_contracts.is_deleted '
        'AND offers_billing_contracts.offer_id = ANY ($1) AND '
        '$2 != ANY (offers_billing_contracts.service_types) GROUP BY offers_billing_contracts.offer_id',
        [1, 2],
        'calltracking',
        timeout=3
    )
