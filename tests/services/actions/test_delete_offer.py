import pytest
from cian_test_utils import future

from my_offers import enums
from my_offers.entities import OfferActionRequest, OfferActionResponse
from my_offers.enums.offer_action_status import OfferActionStatus
from my_offers.repositories.monolith_cian_announcementapi.entities import BargainTerms, ObjectModel, Phone
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category
from my_offers.repositories.monolith_cian_realty.entities.announcement_change_status import (
    AnnouncementChangeStatus,
    AnnouncementType,
)
from my_offers.services.actions import delete_offer
from my_offers.services.actions._delete_offer import AnnouncementTypeError, DeleteOfferAction


PATH = 'my_offers.services.actions._delete_offer.'


@pytest.mark.gen_test
async def test_delete_offer(mocker):
    # arrange
    expected = OfferActionResponse(status=OfferActionStatus.ok)
    execute_mock = mocker.patch.object(DeleteOfferAction, 'execute', return_value=future(expected),)

    # act
    result = await delete_offer(OfferActionRequest(offer_id=11), 555)

    # assert
    assert result == expected
    execute_mock.assert_called_once()


class TestDeleteOfferAction:
    @pytest.mark.gen_test
    @pytest.mark.parametrize(
        ('offer_type', 'deal_type', 'expected'),
        (
            (enums.OfferType.flat, enums.DealType.sale, AnnouncementType.flat2),
            (enums.OfferType.flat, enums.DealType.rent, AnnouncementType.flat),
            (enums.OfferType.suburban, enums.DealType.rent, AnnouncementType.suburbian),
            (enums.OfferType.commercial, enums.DealType.rent, AnnouncementType.office),
        )
    )
    def test__get_type_for_asp(self, offer_type, deal_type, expected):
        # arrange
        action = DeleteOfferAction(offer_id=111, user_id=222)

        # act
        result = action._get_type_for_asp(offer_type=offer_type, deal_type=deal_type)

        # assert
        assert result == expected

    def test__get_type_for_asp__not_found__error(self):
        # arrange
        action = DeleteOfferAction(offer_id=111, user_id=222)

        # act & assert
        with pytest.raises(AnnouncementTypeError):
            action._get_type_for_asp(offer_type=enums.OfferType.newobject, deal_type=enums.DealType.sale)

    @pytest.mark.gen_test
    async def test__run_action(self, mocker):
        # arrange
        action = DeleteOfferAction(offer_id=111, user_id=222)
        object_model = ObjectModel(
            id=111,
            bargain_terms=BargainTerms(price=123),
            category=Category.flat_rent,
            phones=[Phone(country_code='1', number='12312')],
            cian_id=333,
        )
        api_announcement_set_deleted_mock = mocker.patch(f'{PATH}api_announcement_set_deleted', return_value=future())

        # act
        await action._run_action(object_model)

        # assert
        api_announcement_set_deleted_mock.assert_called_once_with(
            AnnouncementChangeStatus(
                realty_object_id=111,
                announcement_type=AnnouncementType.flat,
                cian_announcement_id=333,
                cian_user_id=6973754,
            )
        )
