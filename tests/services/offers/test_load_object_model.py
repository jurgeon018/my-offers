import pytest
from cian_test_utils import future
from cian_web.exceptions import BrokenRulesException

from my_offers.repositories.monolith_cian_announcementapi.entities import BargainTerms, ObjectModel, Phone
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category
from my_offers.services.offers import load_object_model


PATH = 'my_offers.services.offers._load_object_model.'


@pytest.mark.gen_test
async def test__load_object_model(mocker):
    # arrange
    expected = ObjectModel(
        id=111,
        bargain_terms=BargainTerms(price=123),
        category=Category.flat_rent,
        phones=[Phone(country_code='1', number='12312')],
        user_id=222,
    )
    get_object_model_mock = mocker.patch(
        f'{PATH}get_object_model',
        return_value=future(expected)
    )
    get_user_filter_mock = mocker.patch(
        f'{PATH}get_user_filter',
        return_value=future({'master_user_id': 123})
    )

    # act
    result = await load_object_model(offer_id=111, user_id=123)

    # assert
    assert result == expected
    get_object_model_mock.assert_called_once_with({
        'offer_id': 111,
        'master_user_id': 123,
    })
    get_user_filter_mock.assert_called_once_with(123)


@pytest.mark.gen_test
async def test__load_object_model__not_found__broken_rule(mocker):
    # arrange
    get_object_model_mock = mocker.patch(
        f'{PATH}get_object_model',
        return_value=future()
    )
    get_user_filter_mock = mocker.patch(
        f'{PATH}get_user_filter',
        return_value=future({'master_user_id': 123})
    )

    # act
    with pytest.raises(BrokenRulesException):
        await load_object_model(offer_id=111, user_id=123)

    # assert
    get_object_model_mock.assert_called_once_with({
        'offer_id': 111,
        'master_user_id': 123,
    })
    get_user_filter_mock.assert_called_once_with(123)
