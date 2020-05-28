import asyncio
from datetime import datetime, timedelta

import pytz
from simple_settings import settings

from my_offers import enums, pg
from my_offers.repositories.postgresql import tables, offers_duplicates
from my_offers.repositories.postgresql.delete import delete_rows_by_offer_id
from my_offers.repositories.postgresql.offer import get_offers_id_older_than


TABLES_TO_DELETE = (
    tables.offers,
    tables.offers_billing_contracts,
    tables.offers_last_import_error,
    tables.offers_offences,
    tables.offers_reindex_queue,
    tables.offers_premoderations,
    offers_duplicates,
)


async def delete_offers_data() -> None:
    while True:
        need_date = datetime.now(tz=pytz.UTC) - timedelta(
            days=settings.COUNT_DAYS_HOLD_DELETED_OFFERS
        )
        offers_to_delete = await get_offers_id_older_than(
            date=need_date,
            status_tab=enums.OfferStatusTab.deleted,
            limit=settings.COUNT_OFFERS_DELETE_IN_ONE_TIME
        )
        if offers_to_delete:
            async with pg.get().transaction():
                for table in TABLES_TO_DELETE:
                    await delete_rows_by_offer_id(
                        table=table,
                        offer_ids=offers_to_delete
                    )
        else:
            await asyncio.sleep(settings.TIMEOUT_BETWEEN_DELETE_OFFERS)
