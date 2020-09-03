import logging
from datetime import datetime
from typing import List

import pytz
from cian_core.context import new_operation_id
from cian_core.rabbitmq.consumer import Message
from cian_core.statsd import statsd

from my_offers.entities import AgentMessage, ModerationOfferOffence, OfferImportError
from my_offers.entities.moderation import OfferPremoderation
from my_offers.helpers.time import get_aware_date
from my_offers.queue.entities import (
    AnnouncementMessage,
    AnnouncementPremoderationReportingMessage,
    NeedUpdateDuplicateMessage,
    OfferNewDuplicateMessage,
    SaveUnloadErrorMessage,
    ServiceContractMessage,
)
from my_offers.repositories.postgresql.offer_premoderation import save_offer_premoderation
from my_offers.services.agents import update_agents_hierarchy
from my_offers.services.announcement import process_announcement
from my_offers.services.billing.contracts_service import (
    mark_to_delete_announcement_contract,
    save_announcement_contract,
)
from my_offers.services.duplicates import send_new_offer_duplicate_notifications, update_offer_duplicates
from my_offers.services.moderation.moderation_service import save_offer_offence
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
                await process_announcement(object_model=object_model, event_date=announcement_message.date)
            except:
                logger.exception('Process announcement error id: %s, key: %s', object_model.id, routing_key)
                raise
            finally:
                statsd.timing(
                    stat='process_announcement_delta',
                    delta=datetime.now(pytz.utc) - get_aware_date(announcement_message.date)
                )


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


async def save_offer_offence_callback(messages: List[Message]) -> None:
    for message in messages:
        offer_offence: ModerationOfferOffence = message.data
        operation_id = offer_offence.operation_id

        with new_operation_id(operation_id):
            await save_offer_offence(offer_offence=offer_offence)


async def save_agent_callback(messages: List[Message]) -> None:
    for message in messages:
        agent: AgentMessage = message.data
        operation_id = agent.operation_id

        with new_operation_id(operation_id):
            await update_agents_hierarchy(agent=agent)


async def save_offer_premoderation_callback(messages: List[Message]) -> None:
    for message in messages:
        premoderation: AnnouncementPremoderationReportingMessage = message.data

        with new_operation_id(premoderation.operation_id):
            await save_offer_premoderation(OfferPremoderation(
                offer_id=premoderation.object_id,
                removed=False,
                row_version=premoderation.row_version,
            ))


async def remove_offer_premoderation_callback(messages: List[Message]) -> None:
    for message in messages:
        premoderation: AnnouncementPremoderationReportingMessage = message.data

        with new_operation_id(premoderation.operation_id):
            await save_offer_premoderation(OfferPremoderation(
                offer_id=premoderation.object_id,
                removed=True,
                row_version=premoderation.row_version,
            ))


async def update_offer_duplicates_callback(messages: List[Message]) -> None:
    for message in messages:
        data: NeedUpdateDuplicateMessage = message.data
        with new_operation_id():
            await update_offer_duplicates(data.id)


async def new_offer_duplicate_notification_callback(messages: List[Message]) -> None:
    for message in messages:
        offer_duplicate: OfferNewDuplicateMessage = message.data

        with new_operation_id(offer_duplicate.operation_id):
            await send_new_offer_duplicate_notifications(offer_duplicate.duplicate_offer_id)
