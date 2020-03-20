import logging
from datetime import datetime

import pytz

from my_offers.entities.billing import AnnouncementBillingContract, OfferBillingContract
from my_offers.repositories import postgresql


logger = logging.getLogger(__name__)


async def save_announcement_contract(billing_contract: AnnouncementBillingContract) -> None:
    """ Сохранить/обновить контракт на услуги по объялвению """

    if not billing_contract.target_object_type.is_announcement:
        return

    if billing_contract.row_version is None:
        logger.error('Contract changed/created without row_version: %s', billing_contract.id)
        return

    now = datetime.now(pytz.utc)
    contract = OfferBillingContract(
        id=billing_contract.id,
        user_id=billing_contract.user_id,
        actor_user_id=billing_contract.actor_user_id,
        publisher_user_id=billing_contract.publisher_user_id,
        offer_id=billing_contract.target_object_id,
        start_date=billing_contract.start_date,
        payed_till=billing_contract.payed_till,
        row_version=billing_contract.row_version,
        is_deleted=False,
        created_at=now,
        updated_at=now
    )
    await postgresql.save_offer_contract(offer_contract=contract)


async def mark_to_delete_announcement_contract(billing_contract: AnnouncementBillingContract) -> None:
    """ Пометить контракт как удаленный.
        Такой контракт будет удален кроном через некоторое время.
    """
    if not billing_contract.target_object_type.is_announcement:
        return

    if billing_contract.row_version is None:
        logger.error('Contract closed without row_version: %s', billing_contract.id)
        return

    await postgresql.set_offer_contract_is_deleted_status(
        contract_id=billing_contract.id,
        row_version=billing_contract.row_version
    )


async def delete_announcement_contract(service_contract: AnnouncementBillingContract) -> None:
    """ Удалить контракт на услуги по объялвению """
    # TODO: https://jira.cian.tech/browse/CD-75463