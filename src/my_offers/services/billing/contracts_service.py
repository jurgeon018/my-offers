import logging
from datetime import datetime

import pytz
from simple_settings import settings

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
        updated_at=now,
        service_types=billing_contract.service_types,
    )
    contract_id = await postgresql.save_offer_contract(offer_contract=contract)
    if contract_id:
        await post_save_contract(contract)


async def post_save_contract(contract: OfferBillingContract) -> None:
    """ Актуализируем данные о мастере и плательщике объявления
        на основе контракта на случай если у агента поменялся мастер.
        Если не удается определить мастера для пользователя контракта,
        то используем в объявлении publisher_id в качестве мастера.
    """
    master_user_id = await postgresql.get_master_user_id(contract.user_id)

    await postgresql.update_offer_master_user_id_and_payed_by(
        offer_id=contract.offer_id,
        master_user_id=master_user_id if master_user_id else contract.publisher_user_id,
        payed_by=contract.publisher_user_id
    )


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
