import pytest
from cian_test_utils import future

from my_offers.entities import OfferActionRequest, OfferActionResponse
from my_offers.enums.offer_action_status import OfferActionStatus
from my_offers.repositories.monolith_cian_announcementapi.entities import (
    ArchiveAnnouncementV2Request,
    BargainTerms,
    ObjectModel,
    Phone,
)
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category
from my_offers.services.actions import archive_offer
from my_offers.services.actions._archive_offer import ArchiveOfferAction


PATH = 'my_offers.services.actions._archive_offer.'


@pytest.mark.gen_test
async def test_archive_offer(mocker):
    # arrange
    expected = OfferActionResponse(status=OfferActionStatus.ok)
    execute_mock = mocker.patch.object(ArchiveOfferAction, 'execute', return_value=future(expected))

    # act
    result = await archive_offer(OfferActionRequest(offer_id=11), 555)

    # assert
    assert result == expected
    execute_mock.assert_called_once()


class TestArchiveOfferAction:

    @pytest.mark.gen_test
    async def test__run_action(self, mocker):
        # arrange
        action = ArchiveOfferAction(offer_id=111, user_id=222)
        object_model = ObjectModel(
            id=111,
            bargain_terms=BargainTerms(price=123),
            category=Category.flat_rent,
            phones=[Phone(country_code='1', number='12312')],
            cian_id=333,
        )

        v2_announcements_archive_mock = mocker.patch(
            f'{PATH}v2_announcements_archive',
            return_value=future()
        )

        # act
        await action._run_action(object_model)

        # assert
        v2_announcements_archive_mock.assert_called_once_with(ArchiveAnnouncementV2Request(announcement_id=111))
