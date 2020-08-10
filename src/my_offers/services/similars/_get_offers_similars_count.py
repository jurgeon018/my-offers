from my_offers import entities


async def v1_get_offers_similars_count(
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
