import pytest
from cian_test_utils import future
from cian_web.exceptions import BrokenRulesException

from my_offers.entities import OfferActionRequest, OfferActionResponse
from my_offers.enums.actions import OfferActionStatus
from my_offers.repositories.monolith_cian_announcementapi.entities import BargainTerms, ObjectModel, Phone
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category
from my_offers.services.actions import update_edit_date
from my_offers.services.actions._update_edit_date import UpdateEditDateOfferAction


PATH = 'my_offers.services.actions._update_edit_date.'


@pytest.mark.gen_test
async def test_update_edit_date(mocker):
    # arrange
    expected = OfferActionResponse(status=OfferActionStatus.ok)
    execute_mock = mocker.patch.object(UpdateEditDateOfferAction, 'execute', return_value=future(expected),)

    # act
    result = await update_edit_date(OfferActionRequest(offer_id=11), 555)

    # assert
    assert result == expected
    execute_mock.assert_called_once()


class TestUpdateEditDateOfferAction:
    @pytest.mark.gen_test
    async def test__run_action(self, mocker):
        # arrange
        action = UpdateEditDateOfferAction(offer_id=111, user_id=222)
        object_model = ObjectModel(
            id=111,
            bargain_terms=BargainTerms(price=123),
            category=Category.flat_rent,
            phones=[Phone(country_code='1', number='12312')],
            cian_id=333,
        )

        update_edit_date_mock = mocker.patch(
            f'{PATH}announcement_api.update_edit_date',
            return_value=future({111: True})
        )

        # act
        await action._run_action(object_model)

        # assert
        update_edit_date_mock.assert_called_once_with([111])

    @pytest.mark.gen_test
    async def test__run_action__not_updated__exception(self, mocker):
        # arrange
        action = UpdateEditDateOfferAction(offer_id=111, user_id=222)
        object_model = ObjectModel(
            id=111,
            bargain_terms=BargainTerms(price=123),
            category=Category.flat_rent,
            phones=[Phone(country_code='1', number='12312')],
            cian_id=333,
        )

        update_edit_date_mock = mocker.patch(
            f'{PATH}announcement_api.update_edit_date',
            return_value=future({111: False})
        )

        # act
        with pytest.raises(BrokenRulesException):
            await action._run_action(object_model)

        # assert
        update_edit_date_mock.assert_called_once_with([111])

    def test__get_action_code(self):
        # arrange
        action = UpdateEditDateOfferAction(offer_id=111, user_id=222)

        # act
        result = action._get_action_code()

        # assert
        assert result == 'can_update_edit_date'
