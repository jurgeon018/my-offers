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
            await process_announcement(raw_offer)
