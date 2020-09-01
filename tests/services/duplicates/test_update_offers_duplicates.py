import pytest
from cian_test_utils import future

from my_offers.services.duplicates import update_offers_duplicates, update_offers_duplicate

PATH = 'my_offers.services.duplicates._update_offer_duplicates.'


@pytest.mark.gen_test
async def test_update_offers_duplicates__no_ids__return(mocker):
    # arrange
    get_offers_row_version_mock = mocker.patch(
        f'{PATH}get_offers_row_version',
        return_value=future()
    )

    # act
    await update_offers_duplicates([])

    # arrange
    get_offers_row_version_mock.assert_not_called()


@pytest.mark.gen_test
async def test_update_offers_duplicates__no_offers__return(mocker):
    # arrange
    get_offers_row_version_mock = mocker.patch(
        f'{PATH}get_offers_row_version',
        return_value=future()
    )

    # act
    await update_offers_duplicates([1])

    # arrange
    get_offers_row_version_mock.assert_called_once_with([1])


@pytest.mark.gen_test
async def test_update_offers_duplicate_no_offers__return(mocker):
    # arrange
    get_offers_row_version_mock = mocker.patch(
        f'{PATH}get_offers_row_version',
        return_value=future()
    )

    # act
    await update_offers_duplicate(1)

    # arrange
    get_offers_row_version_mock.assert_called_once_with([1])
