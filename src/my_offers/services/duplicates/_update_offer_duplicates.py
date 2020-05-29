from typing import List

from simple_settings import settings

from my_offers.queue.producers import offer_new_duplicate_producers
from my_offers.repositories import postgresql
from my_offers.repositories.offers_duplicates import v1_get_offers_duplicates_by_ids
from my_offers.repositories.offers_duplicates.entities import GetOffersDuplicatesByIdsRequest, Offer
from my_offers.repositories.postgresql.offer import get_offers_row_version


async def update_offers_duplicates(offer_ids: List[int]) -> None:
    if not offer_ids:
        return

    offers_row_version = await get_offers_row_version(offer_ids)
    if not offers_row_version:
        return

    request = [Offer(id=item.offer_id, row_version=item.row_version) for item in offers_row_version]
    response = await v1_get_offers_duplicates_by_ids(GetOffersDuplicatesByIdsRequest(request))
    duplicates = response.duplicates

    if duplicates:
        new_duplicates = await postgresql.update_offers_duplicates(duplicates)
        if settings.SEND_PUSH_ON_NEW_DUPLICATE:
            for offer_id in new_duplicates:
                await offer_new_duplicate_producers(offer_id)

    duplicate_ids = {d.offer_id for d in duplicates}
    not_duplicates = list(set(offer_ids) - duplicate_ids)
    if not_duplicates:
        # удалить из дублей если не дубль
        await postgresql.delete_offers_duplicates(not_duplicates)
