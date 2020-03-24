from datetime import datetime

import pytest
from cian_test_utils import future

from my_offers import pg
from my_offers.entities import OfferBillingContract
from my_offers.mappers.billing import offer_billing_contract_mapper
from my_offers.repositories import postgresql


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
    )

    # act
    await postgresql.save_offer_contract(offer_contract=offer_contract)

    # assert
    pg.get().execute.assert_called_once_with(
        'INSERT INTO offers_billing_contracts (id, user_id, actor_user_id, publisher_user_id, offer_id, start_date, '
        'payed_till, row_version, is_deleted, created_at, updated_at) '
        'VALUES ($3, $22, $1, $17, $5, $20, $16, $19, $4, $2, $21) '
        'ON CONFLICT (id) '
        'DO UPDATE SET id = $6, user_id = $8, actor_user_id = $9, publisher_user_id = $10, offer_id = $11, '
        'start_date = $12, payed_till = $13, row_version = $14, is_deleted = $15, updated_at = $7 '
        'WHERE offers_billing_contracts.row_version < $18',
        offer_contract.actor_user_id,
        now,
        offer_contract.id,
        offer_contract.is_deleted,
        offer_contract.offer_id,
        offer_contract.id,
        now,
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
        offer_contract.start_date,
        now,
        offer_contract.user_id
    )


async def test_get_offer_contract(mocker):
    # arrange
    expected_contract_id = 1
    offer_contract = dict(
        id=expected_contract_id,
        user_id=555,
        actor_user_id=777,
        publisher_user_id=888,
        start_date=datetime(2020, 1, 2),
        payed_till=datetime(2020, 2, 2),
        offer_id=999999,
        row_version=0
    )
    pg.get().fetchrow.return_value = future(offer_contract)

    # act
    result = await postgresql.get_offer_contract(offer_id=expected_contract_id)

    # assert
    assert result == offer_billing_contract_mapper.map_from(offer_contract)
    pg.get().fetchrow.assert_called_once_with(
        '\n    select\n        *\n    from\n        offers_billing_contracts\n    where\n        not is_deleted'
        '\n        and offer_id = $1\n    order by\n        row_version desc\n    limit 1\n    ',
        expected_contract_id
    )


async def test_get_offer_contract__contract_is_none(mocker):
    # arrange
    expected_contract_id = 1
    pg.get().fetchrow.return_value = future([])

    # act
    result = await postgresql.get_offer_contract(offer_id=expected_contract_id)

    # assert
    assert result is None
    pg.get().fetchrow.assert_called_once_with(
        '\n    select\n        *\n    from\n        offers_billing_contracts\n    where\n        not is_deleted'
        '\n        and offer_id = $1\n    order by\n        row_version desc\n    limit 1\n    ',
        expected_contract_id
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
