import logging

from my_offers.entities.billing import AnnouncementBillingContract
from my_offers.repositories import postgresql


logger = logging.getLogger(__name__)


async def save_announcement_contract(offer_contract: AnnouncementBillingContract) -> None:
    """ Сохранить/обновить контракт на услуги по объялвению """

    if not offer_contract.target_object_type.is_announcement:
        return

    if offer_contract.row_version is None:
        logger.error('Contract changed/created without row_version: %s', offer_contract.id)
        return

    await postgresql.save_offer_contract(offer_contract=offer_contract)


async def mark_to_delete_announcement_contract(offer_contract: AnnouncementBillingContract) -> None:
    """ Пометить контракт как удаленный.
        Такой контракт будет удален кроном через некоторое время.
    """

    if offer_contract.row_version is None:
        logger.error('Contract closed without row_version: %s', offer_contract.id)
        return

    await postgresql.set_offer_contract_is_deleted_status(
        contract_id=offer_contract.id,
        row_version=offer_contract.row_version
    )


async def delete_announcement_contract(service_contract: AnnouncementBillingContract) -> None:
    """ Удалить контракт на услуги по объялвению """
    # TODO: https://jira.cian.tech/browse/CD-75463
