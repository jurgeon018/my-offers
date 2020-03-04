import pytest
from cian_test_utils import future
from simple_settings import settings

from my_offers.services.offers.clear_offer_service import clear_deleted_offer


@pytest.mark.gen_test
async def test_clear_offer(mocker):

    # arrange
    delete_offers_older_than_mock = mocker.patch(
        'my_offers.services.offers.clear_offer_service.delete_offers_older_than',
        return_value=future(),
    )

    # act
    await clear_deleted_offer()

    # assert
    delete_offers_older_than_mock.assert_called_once_with(settings.COUNT_DAYS_HOLD_DELETED_OFFERS)
