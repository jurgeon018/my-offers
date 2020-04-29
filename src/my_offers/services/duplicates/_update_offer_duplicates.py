from typing import List

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

    new_duplicates = await v1_get_offers_duplicates_by_ids(
        GetOffersDuplicatesByIdsRequest(request)
    )

    await postgresql.update_offers_duplicates(new_duplicates.duplicates)
