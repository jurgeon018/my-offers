import asyncio

from simple_settings import settings

from my_offers import enums, pg
from my_offers.repositories.postgresql.billing import delete_contracts_by_offer_id
from my_offers.repositories.postgresql.moderation import delete_offers_offence_by_offer_id
from my_offers.repositories.postgresql.offer import delete_offers_by_id, get_offers_id_older_than
from my_offers.repositories.postgresql.offer_import_error import delete_import_errors_by_offer_id
from my_offers.repositories.postgresql.offers_reindex_queue import delete_reindex_items


async def delete_offers_data() -> None:
    while True:
        offers_to_delete = await get_offers_id_older_than(
            days_count=settings.COUNT_DAYS_HOLD_DELETED_OFFERS,
            status_tab=enums.OfferStatusTab.deleted,
            limit=settings.COUNT_OFFERS_DELETE_IN_ONE_TIME
        )
        if offers_to_delete:
            async with pg.get().transaction():
                await delete_offers_by_id(offers_to_delete)
                await delete_contracts_by_offer_id(offers_to_delete)
                await delete_import_errors_by_offer_id(offers_to_delete)
                await delete_offers_offence_by_offer_id(offers_to_delete)
                await delete_reindex_items(offers_to_delete)
        else:
            await asyncio.sleep(settings.TIMEOUT_BETWEEN_DELETE_OFFERS)
