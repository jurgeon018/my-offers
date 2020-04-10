from my_offers import entities
from my_offers.repositories import postgresql


async def get_offers_creation_date(request: entities.OffersCreationDateRequest) -> entities.OffersCreationDateResponse:
    if not request.offer_ids:
        return entities.OffersCreationDateResponse(offers=[])

    offers = await postgresql.get_offers_creation_date(
        master_user_id=request.master_user_id,
        offer_ids=request.offer_ids
    )

    return entities.OffersCreationDateResponse(offers=offers)
