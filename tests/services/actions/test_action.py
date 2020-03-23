import pytest
from cian_http.exceptions import ApiClientException, BadRequestException, TimeoutException
from cian_test_utils import future
from cian_web.exceptions import BrokenRulesException

from my_offers import entities
from my_offers.enums.offer_action_status import OfferActionStatus
from my_offers.repositories.monolith_cian_announcementapi.entities import BargainTerms, ObjectModel, Phone
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category
from my_offers.services.actions._action import OfferAction


PATH = 'my_offers.services.actions._action.'


class TestOfferAction:
    @pytest.mark.gen_test
    async def test_execute(self, mocker):
        # arrange
        object_model = mocker.sentinel.object_model
        expected = entities.OfferActionResponse(status=OfferActionStatus.ok)
        load_object_model_mock = mocker.patch.object(
            OfferAction,
            '_load_object_model',
            return_value=future(object_model)
        )
        check_rights_mock = mocker.patch.object(
            OfferAction,
            '_check_rights',
            return_value=future()
        )
        run_action_mock = mocker.patch.object(
            OfferAction,
            '_run_action',
            return_value=future()
        )
        action = OfferAction(offer_id=111, user_id=123)

        # act
        result = await action.execute()

        # assert
        assert result == expected
        load_object_model_mock.assert_called_once()
        check_rights_mock.assert_called_once_with(mocker.ANY, object_model)
        run_action_mock.assert_called_once_with(mocker.ANY, object_model)

    @pytest.mark.gen_test
    async def test_execute__timeout__broken_rules(self, mocker):
        # arrange
        object_model = mocker.sentinel.object_model
        load_object_model_mock = mocker.patch.object(
            OfferAction,
            '_load_object_model',
            return_value=future(object_model)
        )
        check_rights_mock = mocker.patch.object(
            OfferAction,
            '_check_rights',
            return_value=future()
        )
        run_action_mock = mocker.patch.object(
            OfferAction,
            '_run_action',
            return_value=future(exception=TimeoutException(message='zzzz'))
        )
        action = OfferAction(offer_id=111, user_id=123)

        # act
        with pytest.raises(BrokenRulesException):
            await action.execute()

        # assert
        load_object_model_mock.assert_called_once()
        check_rights_mock.assert_called_once_with(mocker.ANY, object_model)
        run_action_mock.assert_called_once_with(mocker.ANY, object_model)

    @pytest.mark.gen_test
    async def test_execute__exception__broken_rules(self, mocker):
        # arrange
        object_model = mocker.sentinel.object_model
        load_object_model_mock = mocker.patch.object(
            OfferAction,
            '_load_object_model',
            return_value=future(object_model)
        )
        check_rights_mock = mocker.patch.object(
            OfferAction,
            '_check_rights',
            return_value=future()
        )
        run_action_mock = mocker.patch.object(
            OfferAction,
            '_run_action',
            return_value=future(exception=BadRequestException(message='zzzz'))
        )
        action = OfferAction(offer_id=111, user_id=123)

        # act
        with pytest.raises(BrokenRulesException):
            await action.execute()

        # assert
        load_object_model_mock.assert_called_once()
        check_rights_mock.assert_called_once_with(mocker.ANY, object_model)
        run_action_mock.assert_called_once_with(mocker.ANY, object_model)

    @pytest.mark.gen_test
    async def test_execute__api_exception__broken_rules(self, mocker):
        # arrange
        object_model = mocker.sentinel.object_model
        load_object_model_mock = mocker.patch.object(
            OfferAction,
            '_load_object_model',
            return_value=future(object_model)
        )
        check_rights_mock = mocker.patch.object(
            OfferAction,
            '_check_rights',
            return_value=future()
        )
        run_action_mock = mocker.patch.object(
            OfferAction,
            '_run_action',
            return_value=future(exception=ApiClientException(message='zzzz'))
        )
        action = OfferAction(offer_id=111, user_id=123)

        # act
        with pytest.raises(BrokenRulesException):
            await action.execute()

        # assert
        load_object_model_mock.assert_called_once()
        check_rights_mock.assert_called_once_with(mocker.ANY, object_model)
        run_action_mock.assert_called_once_with(mocker.ANY, object_model)

    @pytest.mark.gen_test
    async def test__run_action(self, mocker):
        # arrange
        action = OfferAction(offer_id=111, user_id=123)

        # act & assert
        with pytest.raises(NotImplementedError):
            await action._run_action(mocker.sentinel.object_model)

    @pytest.mark.gen_test
    async def test__check_rights(self):
        # arrange
        action = OfferAction(offer_id=111, user_id=123)
        object_model = ObjectModel(
            id=111,
            bargain_terms=BargainTerms(price=123),
            category=Category.flat_rent,
            phones=[Phone(country_code='1', number='12312')],
            user_id=222,
        )

        # act & assert
        with pytest.raises(BrokenRulesException):
            await action._check_rights(object_model)

    @pytest.mark.gen_test
    async def test__load_object_model(self, mocker):
        # arrange
        action = OfferAction(offer_id=111, user_id=123)
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
        get_master_user_filter_mock = mocker.patch(
            f'{PATH}get_master_user_filter',
            return_value=future([123])
        )

        # act
        result = await action._load_object_model()

        # assert
        assert result == expected
        get_object_model_mock.assert_called_once_with({
            'offer_id': 111,
            'master_user_id': [123],
        })
        get_master_user_filter_mock.assert_called_once_with(123)

    @pytest.mark.gen_test
    async def test__load_object_model__not_found__broken_rule(self, mocker):
        # arrange
        action = OfferAction(offer_id=111, user_id=123)
        get_object_model_mock = mocker.patch(
            f'{PATH}get_object_model',
            return_value=future()
        )
        get_master_user_filter_mock = mocker.patch(
            f'{PATH}get_master_user_filter',
            return_value=future([123])
        )

        # act
        with pytest.raises(BrokenRulesException):
            await action._load_object_model()

        # assert
        get_object_model_mock.assert_called_once_with({
            'offer_id': 111,
            'master_user_id': [123],
        })
        get_master_user_filter_mock.assert_called_once_with(123)
