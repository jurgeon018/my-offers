import asyncio
import logging
from datetime import datetime
from itertools import chain
from typing import Iterable, List, NamedTuple, Set

import pytz
from cian_core.context import new_operation_id
from more_itertools import grouper
from simple_settings import settings

from my_offers.entities import OfferRowVersion
from my_offers.repositories import monolith_cian_elasticapi, postgresql
from my_offers.repositories.monolith_cian_elasticapi.entities import (
    ApiElasticAnnouncementV3GetChangedIds,
    ElasticAnnouncementRowVersion,
)
from my_offers.services.realty_resender._jobs import run_resend_task, save_offers_from_elasticapi


logger = logging.getLogger()


class _OffersDiff(NamedTuple):
    not_found: Iterable[int]
    """Объявления не найденный в my=offers, но притутсвующие в Realty.Objects"""
    need_update: Iterable[int]
    """Объявления для которых не совпадают версии строк"""


async def resend_offers(bulk_size: int) -> None:
    """ Догоняет и проверяет сходимость объявлений в Realty.Objects и my-offers.offers.

        Алгоритм имеет два режима работы:
            1. Через шедулер шарпа (делаем запрос на получение объявок через очередь)
            2. Через апи щарпа на стороне my-offers (поход за объявлением в elasticapi и сохранение через очередь)

        Каждый прогон вычисляет max(row_version) от всех полученных объявлений.
        Следующий прогон начнется с последнего сохранненого row_version.
    """
    bulk_size = settings.SYNC_OFFERS_GET_DIFF_BULK_SIZE or bulk_size
    row_version = await postgresql.get_last_row_version()

    with new_operation_id() as operation_id:
        changed_offers = await monolith_cian_elasticapi.api_elastic_announcement_v3_get_changed_ids(
            ApiElasticAnnouncementV3GetChangedIds(row_version=row_version, top=settings.SYNC_OFFERS_TOP_CHANGED_CNT)
        )
        changed_offers_len = len(changed_offers)
        max_row_version = max(x.row_version for x in changed_offers) - settings.SYNC_OFFERS_ROW_VERSION_OFFSET

        logger.info('Get changed offers from row_version: %s, count: %s', row_version, changed_offers_len)
        logger.info('Max row version found: %s', max_row_version)

        diffs = []
        offers_progress = 0
        for offers in grouper(changed_offers, bulk_size):
            offers = list(filter(None, offers))  # type: ignore
            offers_progress += len(offers)

            logger.info('Get offers diff, progress %s/%s', offers_progress, changed_offers_len)
            await asyncio.sleep(settings.SYNC_OFFERS_GET_DIFF_DELAY)
            offers_diff = await _get_offers_diff(changed_offers=offers)  # type: ignore
            diffs.append(offers_diff)

        need_update = list(chain(*[d.need_update for d in diffs]))
        not_found_in_db = list(chain(*[d.not_found for d in diffs]))
        offers_ids = [
            *need_update,
            *not_found_in_db
        ]
        if settings.SYNC_OFFERS_ALLOW_RUN_TASK:
            await run_resend_task(offers_ids=offers_ids)
        else:
            await save_offers_from_elasticapi(offers_ids=offers_ids)

        now = datetime.now(tz=pytz.utc)
        await postgresql.save_cron_session(
            operation_id=operation_id,
            row_version=max_row_version,
            created_at=now
        )
        await postgresql.save_cron_stats(
            operation_id=operation_id,
            founded_from_elastic=changed_offers_len,
            need_update=len(need_update),
            not_found_in_db=len(not_found_in_db),
            created_at=now
        )


async def _get_offers_diff(changed_offers: List[ElasticAnnouncementRowVersion]) -> _OffersDiff:
    realty_offers_set = set(o.realty_object_id for o in changed_offers)
    my_offers_ids = await postgresql.get_offers_row_version(offer_ids=realty_offers_set)
    my_offers_set = {o.offer_id for o in my_offers_ids}

    # объявления, которых нет в my_offers
    difference_for_my_offers = realty_offers_set - my_offers_set

    # объявления, которые отстали по версиям от Realty.Objects
    difference_for_rows_versions = _get_row_versions_diff(changed_offers, my_offers_ids)

    return _OffersDiff(
        not_found=difference_for_my_offers,
        need_update=difference_for_rows_versions,
    )


def _get_row_versions_diff(
        realty_offers: List[ElasticAnnouncementRowVersion],
        my_offers: List[OfferRowVersion]
) -> Set[int]:
    my_offers_map = {o.offer_id: o for o in my_offers}
    found_difference = set()

    for realty_offer in realty_offers:
        offer_id = realty_offer.realty_object_id
        my_offer = my_offers_map.get(offer_id)

        if not my_offer:
            continue

        if realty_offer.row_version > my_offer.row_version:
            found_difference.add(offer_id)

    return found_difference
