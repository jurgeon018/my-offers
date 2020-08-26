from my_offers.repositories.postgresql.object_model import get_object_model
from my_offers.repositories.postgresql.offers_duplicates import get_offer_duplicates
from my_offers.services.notifications import send_duplicates_notification


async def send_new_offer_duplicate_notifications(duplicate_offer_id: int) -> None:
    """ Послать новое уведомляние по дубликату объявления """
    limit = 100
    offset = 0

    duplicate_offer = await get_object_model({'offer_id': duplicate_offer_id})
    if not duplicate_offer or not duplicate_offer.status.is_published:
        return

    while True:
        duplicates = await get_offer_duplicates(
            offer_id=duplicate_offer_id,
            limit=limit,
            offset=offset,
        )
        offset += limit
        if not duplicates:
            break

        for offer, _ in duplicates:
            user_id = offer.published_user_id
            if user_id == duplicate_offer.published_user_id:
                continue

            await send_duplicates_notification(offer=offer, duplicate_offer=duplicate_offer, user_id=user_id)
