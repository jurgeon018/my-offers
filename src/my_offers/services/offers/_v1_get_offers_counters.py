from my_offers import entities
from my_offers.repositories.postgresql.offer import get_offer_counters
from my_offers.services.offers import get_user_filter


async def v1_get_offers_counters_public(realty_user_id: int) -> entities.OfferCounters:
    filters = await get_user_filter(realty_user_id)

    return await get_offer_counters(filters)
