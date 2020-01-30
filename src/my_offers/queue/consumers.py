import logging
from typing import List

from cian_core.context import new_operation_id
from cian_core.rabbitmq.consumer import Message

from my_offers.queue.entities import AnnouncementMessage
from my_offers.services.announcement.process_announcement import process_announcement


logger = logging.getLogger(__name__)


async def process_announcement_callback(messages: List[Message]) -> None:
    for message in messages:
        announcement_message: AnnouncementMessage = message.data
        with new_operation_id(operation_id=announcement_message.operation_id):
            try:
                await process_announcement(announcement_message.model)
            except Exception:
                logger.warning('Process error', exc_info=True)
