import pytest
from cian_test_utils import future
from simple_settings.utils import settings_stub

from my_offers.services.duplicates import sync_offer_duplicates


PATH = 'my_offers.services.duplicates._sync_offer_duplicates.'


async def test_sync_offer_duplicates(mocker):
    # arrange
    get_offer_duplicate_for_update_mock = mocker.patch(
        f'{PATH}offers_duplicates.get_offer_duplicate_for_update',
        side_effect=[
            future(1),
            Exception(),
        ]
    )
    update_offer_duplicates_mock = mocker.patch(
        f'{PATH}duplicates.update_offer_duplicates',
        return_value=future()
    )

    # act
    with pytest.raises(Exception):
        await sync_offer_duplicates()

    # assert
    get_offer_duplicate_for_update_mock.assert_called()
    update_offer_duplicates_mock.assert_called_once_with(1)


async def test_sync_offer_duplicates__no_data__sleep(mocker):
    # arrange
    get_offer_duplicate_for_update_mock = mocker.patch(
        f'{PATH}offers_duplicates.get_offer_duplicate_for_update',
        side_effect=[
            future(None),
            Exception(),
        ]
    )
    update_offer_duplicates_mock = mocker.patch(
        f'{PATH}duplicates.update_offer_duplicates',
        return_value=future()
    )
    sleep_mock = mocker.patch(
        f'{PATH}asyncio.sleep',
        return_value=future(None)
    )

    # act
    with pytest.raises(Exception), settings_stub(SYNC_OFFER_DUPLICATES_TIMEOUT=77):
        await sync_offer_duplicates()

    # assert
    get_offer_duplicate_for_update_mock.assert_called()
    update_offer_duplicates_mock.assert_not_called()
    sleep_mock.assert_called_once_with(77)
