from datetime import datetime

import pytest
from cian_test_utils import future, v

from my_offers.entities.billing import AnnouncementBillingContract
from my_offers.enums import TargetObjectType
from my_offers.services.billing.contracts_service import (
    mark_to_delete_announcement_contract,
    save_announcement_contract,
)


pytestmark = pytest.mark.gen_test


async def test_save_announcement_contract(mocker):
    # arrange
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
        row_version=0
    ))
    save_offer_contract_mock = mocker.patch(
        'my_offers.services.billing.contracts_service.postgresql.save_offer_contract',
        return_value=future()
    )

    # act
    await save_announcement_contract(offer_contract=offer_contract)

    # assert
    save_offer_contract_mock.assert_called_with(offer_contract=offer_contract)


async def test_save_announcement_contract__row_version_is_none(mocker):
    # arrange
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
        row_version=None
    ))
    logger = mocker.patch(
        'my_offers.services.billing.contracts_service.logger',
        return_value=future()
    )

    # act
    await save_announcement_contract(offer_contract=offer_contract)

    # assert
    logger.error.assert_called_with('Contract changed/created without row_version: %s', offer_contract.id)


@pytest.mark.parametrize('target_object_type', [
    TargetObjectType.announcement_lite,
    TargetObjectType.account,
    TargetObjectType.account_subscription,
    TargetObjectType.account_service_package,
    TargetObjectType.penalty,
    TargetObjectType.order_cancellation,
    TargetObjectType.order_transfer,
    TargetObjectType.tech_spend,
    TargetObjectType.tech_transfer,
    TargetObjectType.expired_bonus_wallet,
    TargetObjectType.post_paid,
    TargetObjectType.demand,
    TargetObjectType.demand_package,
])
async def test_save_announcement_contract__ignore_types(mocker, target_object_type):
    # arrange
    offer_contract = v(AnnouncementBillingContract(
        id=1,
        user_id=666,
        actor_user_id=777,
        publisher_user_id=888,
        start_date=datetime(2020, 1, 2),
        payed_till=datetime(2020, 2, 2),
        target_object_id=999999,
        target_object_type=target_object_type,
        service_types=[],
        row_version=321332123
    ))
    save_offer_contract_mock = mocker.patch(
        'my_offers.services.billing.contracts_service.postgresql.save_offer_contract',
        return_value=future()
    )

    # act
    await save_announcement_contract(offer_contract=offer_contract)

    # assert
    save_offer_contract_mock.assert_not_called()


async def test_mark_to_delete_announcement_contract(mocker):
    # arrange
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
        row_version=0
    ))
    set_offer_contract_is_deleted_status_mock = mocker.patch(
        'my_offers.services.billing.contracts_service.postgresql.set_offer_contract_is_deleted_status',
        return_value=future()
    )

    # act
    await mark_to_delete_announcement_contract(offer_contract=offer_contract)

    # assert
    set_offer_contract_is_deleted_status_mock.assert_called_with(
        contract_id=offer_contract.id,
        row_version=offer_contract.row_version
    )


async def test_mark_to_delete_announcement_contract__row_version_is_none(mocker):
    # arrange
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
        row_version=None
    ))
    logger = mocker.patch(
        'my_offers.services.billing.contracts_service.logger',
        return_value=future()
    )

    # act
    await mark_to_delete_announcement_contract(offer_contract=offer_contract)

    # assert
    logger.error.assert_called_with('Contract closed without row_version: %s', offer_contract.id)
