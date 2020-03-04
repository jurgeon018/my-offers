from simple_settings import settings

from my_offers.repositories.postgresql.offer import delete_offers_older_than


async def clear_deleted_offer() -> None:
    await delete_offers_older_than(settings.COUNT_DAYS_HOLD_DELETED_OFFERS)
