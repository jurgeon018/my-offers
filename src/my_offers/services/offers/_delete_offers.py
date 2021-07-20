import asyncio
import logging
from datetime import datetime, timedelta
from typing import List

import pytz
from cian_core.statsd import statsd
from simple_settings import settings

from my_offers import pg
from my_offers.enums import OfferStatusTab
from my_offers.repositories import postgresql
from my_offers.repositories.postgresql import tables
from my_offers.repositories.postgresql.delete import delete_rows_by_offer_id
from my_offers.repositories.postgresql.offers_delete_queue import offers_delete_queue
from my_offers.repositories.postgresql.offers_duplicate_notification import offers_duplicate_notification
from my_offers.repositories.postgresql.offers_duplicates import offers_duplicates
from my_offers.repositories.postgresql.offers_similars import offers_similars_flat, offers_similars_test


logger = logging.getLogger(__name__)


TABLES_TO_DELETE = (
    tables.offers_billing_contracts,
    offers_duplicates,
    tables.offers_last_import_error,
    tables.offers_offences,
    tables.offers_premoderations,
    tables.offers_reindex_queue,
    tables.offer_relevance_warnings,
    offers_similars_flat,
    offers_similars_test,
    offers_duplicate_notification,
)


async def delete_offers_data() -> None:
    while True:
        try:
            while offer_ids := await postgresql.get_offer_ids_for_delete(
                limit=settings.COUNT_OFFERS_DELETE_IN_ONE_TIME,
                timeout=settings.DB_TIMEOUT_DELETE_OFFERS,
            ):
                async with pg.get().transaction():
                    await delete_rows_by_offer_id(
                        table=offers_delete_queue,
                        offer_ids=offer_ids,
                        timeout=settings.DB_TIMEOUT_DELETE_OFFERS,
                    )
                    offers_to_delete = await postgresql.delete_offers(
                        offer_ids=offer_ids,
                        timeout=settings.DB_TIMEOUT_DELETE_OFFERS,
                    )

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


async def delete_offers(offer_ids: List[int]) -> None:
    await postgresql.set_offers_status_tab(offer_ids, OfferStatusTab.deleted)
    await postgresql.add_offer_to_delete_queue(
        offer_ids=offer_ids,
        delete_at=datetime.now(tz=pytz.UTC) + timedelta(days=settings.COUNT_DAYS_HOLD_DELETED_OFFERS)
    )
