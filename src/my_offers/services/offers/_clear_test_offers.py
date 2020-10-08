from simple_settings import settings

from my_offers.repositories import postgresql


async def clear_test_offers() -> None:
    await postgresql.clear_test_offers(settings.SKIP_TEST_USER_IDS_DELETE_OFFERS)