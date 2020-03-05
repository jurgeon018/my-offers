import logging
from typing import List

from cian_core.context import new_operation_id
from cian_core.rabbitmq.consumer import Message
from cian_core.statsd import statsd

from my_offers.entities import OfferImportError
from my_offers.queue.entities import AnnouncementMessage, SaveUnloadErrorMessage, ServiceContractMessage
from my_offers.services.announcement import process_announcement
from my_offers.services.billing.contracts_service import (
    mark_to_delete_announcement_contract,
    save_announcement_contract,
)
from my_offers.services.offers_import import save_offers_import_error


logger = logging.getLogger(__name__)


async def process_announcement_callback(messages: List[Message]) -> None:
    for message in messages:
        announcement_message: AnnouncementMessage = message.data
        object_model = announcement_message.model
        operation_id = announcement_message.operation_id
        routing_key = message.envelope.routing_key
        with new_operation_id(operation_id), statsd.timer(f'queue.{routing_key}'):
            try:
                await process_announcement(object_model)
            except:
                logger.exception('Process announcement error id: %s, key: %s', object_model.id, routing_key)
                raise


async def save_announcement_contract_callback(messages: List[Message]) -> None:
    for message in messages:
        contract_message: ServiceContractMessage = message.data
        operation_id = contract_message.operation_id
        offer_contract = contract_message.service_contract_reporting_model

        with new_operation_id(operation_id):
            await save_announcement_contract(billing_contract=offer_contract)


async def mark_to_delete_announcement_contract_callback(messages: List[Message]) -> None:
    for message in messages:
        contract_message: ServiceContractMessage = message.data
        operation_id = contract_message.operation_id
        offer_contract = contract_message.service_contract_reporting_model

        with new_operation_id(operation_id):
            await mark_to_delete_announcement_contract(billing_contract=offer_contract)


async def save_offer_unload_error_callback(messages: List[Message]) -> None:
    errors = {}
    for message in messages:
        error_message: SaveUnloadErrorMessage = message.data
        if not error_message.object_id:
            continue
        errors[error_message.object_id] = OfferImportError(
            offer_id=error_message.object_id,
            type=error_message.error.type,
            message=error_message.error.message,
            created_at=error_message.date,
        )

    if errors:
        with new_operation_id():
            await save_offers_import_error(list(errors.values()))
