import pytest
from cian_test_utils import future
from cian_web.exceptions import BrokenRulesException

from my_offers.entities.qa import QaGetByIdRequest
from my_offers.services.qa import get_offer, get_offer_view


@pytest.mark.gen_test
async def test_get_offer(mocker):
    # arrange
    expected = mocker.sentinel.offer
    get_offer_by_id_mock = mocker.patch('my_offers.services.qa.get_offer_by_id', return_value=future(expected))

    # act
    result = await get_offer(QaGetByIdRequest(offer_id=111))

    # assert
    assert result == expected
    get_offer_by_id_mock.assert_called_once_with(111)


@pytest.mark.gen_test
async def test_get_offer__not_found__error(mocker):
    # arrange
    get_offer_by_id_mock = mocker.patch('my_offers.services.qa.get_offer_by_id', return_value=future())

    # act
    with pytest.raises(BrokenRulesException):
        await get_offer(QaGetByIdRequest(offer_id=111))

    # assert
    get_offer_by_id_mock.assert_called_once_with(111)


@pytest.mark.gen_test
async def test_get_offer_view(mocker):
    # arrange
    object_model = mocker.sentinel.object_model
    offer_view = mocker.sentinel.offer_view
    build_offer_view_mock = mocker.patch(
        'my_offers.services.qa.get_offer_views',
        return_value=future(([offer_view], {}))
    )

    get_object_model_by_id_mock = mocker.patch(
        'my_offers.services.qa.get_object_model_by_id',
        return_value=future(object_model)
    )

    # act
    result = await get_offer_view(QaGetByIdRequest(offer_id=111))

    # assert
    assert result == offer_view
    get_object_model_by_id_mock.assert_called_once_with(111)
    build_offer_view_mock.assert_called_once_with([object_model])


@pytest.mark.gen_test
async def test_get_offer_view__not_found__error(mocker):
    # arrange
    get_object_model_by_id_mock = mocker.patch('my_offers.services.qa.get_object_model_by_id', return_value=future())

    # act
    with pytest.raises(BrokenRulesException):
        await get_offer_view(QaGetByIdRequest(offer_id=111))

    # assert
    get_object_model_by_id_mock.assert_called_once_with(111)
