import logging
from typing import List

from cian_core.context import new_operation_id
from cian_core.rabbitmq.consumer import Message

from my_offers.queue.entities import AnnouncementMessage, ServiceContractMessage
from my_offers.services.announcement import process_announcement
from my_offers.services.billing.contracts_service import (
    mark_to_delete_announcement_contract,
    save_announcement_contract,
)


logger = logging.getLogger(__name__)


async def process_announcement_callback(messages: List[Message]) -> None:
    for message in messages:
        announcement_message: AnnouncementMessage = message.data
        raw_offer = announcement_message.model
        if not raw_offer.get('rowVersion'):
            # todo: подумать как обработать такой случай CD-73846
            logger.exception(
                'Row version not found offerId: %s key: %s',
                raw_offer.get('id'),
                message.envelope.routing_key,
            )
            continue
        with new_operation_id(announcement_message.operation_id):
            try:
                await process_announcement(raw_offer)
            except:
                # todo: https://jira.cian.tech/browse/CD-73846 - обработка ошибок
                logger.exception(
                    'Announcement process error: %s key: %s',
                    raw_offer.get('id'),
                    message.envelope.routing_key,
                )
                raise


async def save_announcement_contract_callback(messages: List[Message]) -> None:
    for message in messages:
        contract_message: ServiceContractMessage = message.data
        operation_id = contract_message.operation_id
        offer_contract = contract_message.service_contract_reporting_model

        with new_operation_id(operation_id):
            await save_announcement_contract(offer_contract=offer_contract)


async def mark_to_delete_announcement_contract_callback(messages: List[Message]) -> None:
    for message in messages:
        contract_message: ServiceContractMessage = message.data
        operation_id = contract_message.operation_id
        offer_contract = contract_message.service_contract_reporting_model

        with new_operation_id(operation_id):
            await mark_to_delete_announcement_contract(offer_contract=offer_contract)
