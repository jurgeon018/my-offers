import asyncio
import logging
from typing import List

from cian_core.statsd import statsd
from simple_settings import settings

from my_offers.queue.producers import offer_new_duplicate_producers
from my_offers.repositories import postgresql
from my_offers.repositories.offers_duplicates import v1_get_offers_duplicates_by_ids
from my_offers.repositories.offers_duplicates.entities import Duplicate, GetOffersDuplicatesByIdsRequest, Offer
from my_offers.repositories.postgresql import offers_similars
from my_offers.repositories.postgresql.offer import get_offers_row_version


logger = logging.getLogger(__name__)


async def update_offers_duplicate(offer_id: int) -> None:
    offers_row_version = await get_offers_row_version([offer_id])
    if not offers_row_version:
        return

    duplicates: List[Duplicate] = await _get_duplicates(offers_row_version)

    if duplicates:
        duplicate = duplicates[0]
        duplicate_offer_id = duplicate.offer_id
        group_id = duplicate.duplicate_group_id
        is_new = await postgresql.update_offers_duplicate(
            offer_id=duplicate_offer_id,
            group_id=group_id,
            row_version=offers_row_version[0].row_version
        )
        is_valid = await _check_duplicates_group(offer_id=duplicate_offer_id, group_id=group_id)
        if is_new and is_valid:
                await _on_new_duplicates([duplicate_offer_id])
    else:
        await _on_remove_duplicates([offer_id])


async def update_offers_duplicates(offer_ids: List[int]) -> None:
    if not offer_ids:
        return

    offers_row_version = await get_offers_row_version(offer_ids)
    if not offers_row_version:
        return

    duplicates: List[Duplicate] = await _get_duplicates(offers_row_version)
    if duplicates:
        new_duplicates = await postgresql.update_offers_duplicates(duplicates)
        if new_duplicates:
            await _on_new_duplicates(new_duplicates)

    duplicate_ids = {d.offer_id for d in duplicates}
    not_duplicates = list(set(offer_ids) - duplicate_ids)
    if not_duplicates:
        await _on_remove_duplicates(not_duplicates)


async def _get_duplicates(offers_row_version) -> List[Duplicate]:
    request = [Offer(id=item.offer_id, row_version=item.row_version) for item in offers_row_version]
    response = await v1_get_offers_duplicates_by_ids(GetOffersDuplicatesByIdsRequest(request))

    return response.duplicates


async def _on_new_duplicates(offer_ids: List[int]) -> None:
    await offers_similars.update_group_id(offer_ids)
    await _send_push(offer_ids)


async def _on_remove_duplicates(offer_ids: List[int]) -> None:
    # удалить из дублей если не дубль
    await postgresql.delete_offers_duplicates(offer_ids)
    await offers_similars.unset_group_id(offer_ids)


async def _send_push(offer_ids: List[int]) -> None:
    if settings.SEND_PUSH_ON_NEW_DUPLICATE:
        for offer_id in offer_ids:
            await offer_new_duplicate_producers(offer_id)


async def _check_duplicates_group(*, offer_id: int, group_id: int) -> bool:
    main_similar, similar_group = await asyncio.gather(
        offers_similars.get_offer_similar(offer_id),
        offers_similars.get_offers_similars_by_group_id(group_id),
    )

    if not main_similar:
        logger.warning('Similar not found offer_id %s', offer_id)
        statsd.incr('new_duplicate_offer.not_valid.not_found')
        return False

    for similar in similar_group:
        if main_similar.district_id != similar.district_id:
            logger.warning('Wrong region offer_id %s similar %s', offer_id, similar.offer_id)
            statsd.incr('new_duplicate_offer.not_valid.wrong_region')
            return False
        if abs(main_similar.rooms_count - similar.rooms_count) > settings.SIMILAR_ROOM_DELTA:
            logger.warning('Wrong rooms_count offer_id %s similar %s', offer_id, similar.offer_id)
            statsd.incr('new_duplicate_offer.not_valid.wrong_rooms_count')
            return False
        if abs(main_similar.price - similar.price) / main_similar.price > settings.SIMILAR_PRICE_KF:
            logger.warning('Wrong rooms_count offer_id %s similar %s', offer_id, similar.offer_id)
            statsd.incr('new_duplicate_offer.not_valid.wrong_rooms_count')
            return False

    statsd.incr('new_duplicate_offer.valid')

    return True
