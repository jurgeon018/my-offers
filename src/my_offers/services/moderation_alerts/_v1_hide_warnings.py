from my_offers import entities
from my_offers.repositories.postgresql import save_last_visit_date


async def v1_hide_warnings_public(
        request: entities.MobileGetMyOffersRequest,
        realty_user_id: int
) -> None:
    await save_last_visit_date(realty_user_id)

    return None
