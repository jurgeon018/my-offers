import asyncio

from cian_core.context import new_operation_id
from simple_settings import settings

from my_offers.services.duplicates import update_offer_duplicates


async def sync_offer_duplicates() -> None:
    while True:
        offer_id = await get_offer_duplicate_for_update()
        if offer_id:
            with new_operation_id():
                await update_offer_duplicates(offer_id)
        else:
            await asyncio.sleep(settings.SYNC_OFFER_DUPLICATES_TIMEOUT)