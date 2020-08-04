import pytest
from cian_test_utils import future

from my_offers.entities import GetOfferDuplicatesRequest
from my_offers.enums import DuplicateTabType
from my_offers.repositories.monolith_cian_announcementapi.entities import BargainTerms, Geo
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category, ObjectModel, Status
from my_offers.services.duplicates._get_offer_duplicates import v1_get_offer_duplicates_public
from my_offers.helpers.similar import is_offer_for_similar


@pytest.mark.parametrize(
    ('status', 'category', 'expected'),
    (
        (Status.deactivated, Category.flat_sale, False),
        (Status.published, Category.flat_sale, True),
        (Status.published, Category.daily_flat_rent, False),
    )
)
def test_validate_offer(status, category, expected):
    # arrange & act
    result = is_offer_for_similar(status=status, category=category)

    # assert
    assert result == expected


class TestNoSelectOffersInBdWithZeroCount:
    PATH = 'my_offers.services.duplicates._get_offer_duplicates.'

    object_model = ObjectModel(
        id=999,
        bargain_terms=BargainTerms(price=123),
        category=Category.flat_rent,
        phones=[],
        geo=Geo(district=None),
    )

    @pytest.mark.parametrize(
        ('func_for_check', 'tab'),
        (
            ('get_offers_in_same_building', DuplicateTabType.same_building),
            ('get_similar_offers', DuplicateTabType.similar),
            ('get_offer_duplicates', DuplicateTabType.duplicate)
        )
    )
    async def test_tab_with_zero_offers_count(self, func_for_check, tab, mocker):
        # arrange
        mocker.patch(
            f'{self.PATH}load_object_model',
            return_value=future(self.object_model)
        )
        mocker.patch(
            f'{self.PATH}validate_offer',
            return_value=future(True)
        )
        mocker.patch(
            f'{self.PATH}get_offer_duplicates_ids',
            return_value=future([])
        )
        mocker.patch(
            f'{self.PATH}get_offers_in_same_building_count',
            return_value=future(0)
        )
        mocker.patch(
            f'{self.PATH}get_similar_offers_count',
            return_value=future(0)
        )
        func_for_check_mock = mocker.patch(
            f'{self.PATH}{func_for_check}',
            return_value=future([])
        )

        # act
        await v1_get_offer_duplicates_public(
            request=GetOfferDuplicatesRequest(
                offer_id=999,
                type=tab,
                pagination=None
            ),
            realty_user_id=111,
        )

        # assert
        func_for_check_mock.assert_not_called()

    async def test_tab_all_with_zero_offers_count(self, mocker):
        # arrange
        mocker.patch(
            f'{self.PATH}load_object_model',
            return_value=future(self.object_model)
        )
        mocker.patch(
            f'{self.PATH}validate_offer',
            return_value=future(True)
        )
        mocker.patch(
            f'{self.PATH}get_offer_duplicates_ids',
            return_value=future([])
        )
        mocker.patch(
            f'{self.PATH}get_offers_in_same_building_count',
            return_value=future(0)
        )
        mocker.patch(
            f'{self.PATH}get_similar_offers_count',
            return_value=future(0)
        )
        get_offer_duplicates_mock = mocker.patch(
            f'{self.PATH}get_offer_duplicates',
            return_value=future([])
        )
        get_offers_in_same_building_mock = mocker.patch(
            f'{self.PATH}get_offers_in_same_building',
            return_value=future([])
        )
        get_similar_offers_mock = mocker.patch(
            f'{self.PATH}get_similar_offers',
            return_value=future([])
        )

        # act
        await v1_get_offer_duplicates_public(
            request=GetOfferDuplicatesRequest(
                offer_id=999,
                type=DuplicateTabType.all,
                pagination=None
            ),
            realty_user_id=111,
        )

        # assert
        get_offer_duplicates_mock.assert_not_called()
        get_offers_in_same_building_mock.assert_not_called()
        get_similar_offers_mock.assert_not_called()
