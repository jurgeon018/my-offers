import logging
from typing import List

from cian_core.context import new_operation_id
from cian_core.rabbitmq.consumer import Message

from my_offers.queue.entities import AnnouncementMessage
from my_offers.services.announcement import process_announcement


logger = logging.getLogger(__name__)


async def process_announcement_callback(messages: List[Message]) -> None:
    for message in messages:
        announcement_message: AnnouncementMessage = message.data
        object_model = announcement_message.model
        if not object_model.row_version:
            # todo: подумать как обработать такой случай CD-73846
            logger.exception(
                'Row version not found offerId: %s key: %s',
                object_model.id,
                message.envelope.routing_key,
            )
            continue
        with new_operation_id(announcement_message.operation_id):
            await process_announcement(object_model)
