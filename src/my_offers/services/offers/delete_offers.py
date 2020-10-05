import asyncio
import logging
from datetime import datetime, timedelta

import pytz
from cian_core.statsd import statsd
from simple_settings import settings

from my_offers import enums, pg
from my_offers.repositories.postgresql import tables
from my_offers.repositories.postgresql.delete import delete_rows_by_offer_id
from my_offers.repositories.postgresql.offer import get_offers_id_older_than
from my_offers.repositories.postgresql.offers_duplicates import offers_duplicates


logger = logging.getLogger(__name__)


TABLES_TO_DELETE = (
    tables.offers,
    tables.offers_billing_contracts,
    offers_duplicates,
    tables.offers_last_import_error,
    tables.offers_offences,
    tables.offers_premoderations,
    tables.offers_reindex_queue,
)


async def delete_offers_data() -> None:
    while True:
        need_date = datetime.now(tz=pytz.UTC) - timedelta(
            days=settings.COUNT_DAYS_HOLD_DELETED_OFFERS
        )
        try:
            while offers_to_delete := await get_offers_id_older_than(
                date=need_date,
                status_tab=enums.OfferStatusTab.deleted,
                limit=settings.COUNT_OFFERS_DELETE_IN_ONE_TIME,
                timeout=settings.DB_TIMEOUT_DELETE_OFFERS,
            ):
                async with pg.get().transaction():
                    for table in TABLES_TO_DELETE:
                        await delete_rows_by_offer_id(
                            table=table,
                            offer_ids=offers_to_delete,
                            timeout=settings.DB_TIMEOUT_DELETE_OFFERS,
                        )
                    statsd.incr('delete_offers_count', len(offers_to_delete))
        except asyncio.exceptions.TimeoutError:
            logger.exception('Delete offers timeout')

        await asyncio.sleep(settings.TIMEOUT_BETWEEN_DELETE_OFFERS)
