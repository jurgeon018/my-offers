from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel
from my_offers.repositories.postgresql.object_model import get_object_model
from my_offers.repositories.postgresql.offers_duplicates import get_offer_duplicates


async def send_new_offer_duplicate_notifications(duplicate_offer_id: int) -> None:
    limit = 100
    offset = 0

    duplicate_offer = await get_object_model({'offer_id': duplicate_offer_id})
    if not duplicate_offer or not duplicate_offer.status.is_published:
        return

    while True:
        duplicates, _ = await get_offer_duplicates(
            offer_id=duplicate_offer_id,
            limit=limit,
            offset=offset,
        )
        offset += limit
        if not duplicates:
            break

        for offer in duplicates:
            process_notification(offer=offer, duplicate_offer=duplicate_offer)


async def process_notification(*, offer: ObjectModel, duplicate_offer: ObjectModel) -> None:

    try:
        await save_notification()
    except:
        # уже отправляли
        return

    try:
        await send_notification()
    except:
        # неполучилось отправить
        await delete_notification()
        raise

    # todo: https://jira.cian.tech/browse/CD-81714 отправить событие для МЛ


async def save_notification():
    pass


async def send_notification():
    pass


async def delete_notification():
    pass
