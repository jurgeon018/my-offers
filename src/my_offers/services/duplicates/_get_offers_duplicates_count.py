from my_offers import entities
from my_offers.repositories.postgresql.offers_duplicates import get_offers_duplicates_count


async def v1_get_offers_duplicates_count(
        request: entities.GetOffersDuplicatesCountRequest
) -> entities.GetOffersDuplicatesCountResponse:
    offer_ids = request.offer_ids
    if not offer_ids:
        return entities.GetOffersDuplicatesCountResponse(
            data=[]
        )

    return entities.GetOffersDuplicatesCountResponse(
        data=await get_offers_duplicates_count(offer_ids)
    )
