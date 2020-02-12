import pytest
from cian_test_utils import future

from my_offers.entities import GetOffersRequest
from my_offers.entities.get_offers import GetOffer, GetOffersResponse, OfferCounters, Statistics
from my_offers.entities.offer_view_model import OfferGeo, PriceInfo
from my_offers.enums import GetOfferStatusTab
from my_offers.repositories.monolith_cian_announcementapi.entities import BargainTerms, ObjectModel, Phone
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category
from my_offers.services import offers


@pytest.mark.gen_test
async def test_get_offer(mocker):
    # arrange
    expected_user = 666
    request = GetOffersRequest(
        status_tab=GetOfferStatusTab.active,
    )
    object_model = ObjectModel(
        bargain_terms=BargainTerms(price=123),
        category=Category.building_rent,
        phones=[
            Phone(country_code='1', number='12312')
        ]
    )
    expected_result = GetOffersResponse(offers=[
        GetOffer(
            main_photo_url=None,
            title=None,
            url=None,
            geo=OfferGeo(address=None, newbuilding=None, underground=None),
            subagent=None,
            price_info=PriceInfo(exact_price='123 ₽/мес.'),
            features=[],
            publish_features=None,
            vas=None,
            is_from_package=False,
            is_manual=False,
            is_publication_time_ends=False,
            created_at=None,
            id=None,
            statistics=Statistics(),
            auction=None
        )],
        counters=OfferCounters(active=1, not_active=0, declined=0, archived=0))

    get_offers_by_status_mock = mocker.patch(
        'my_offers.services.offers.get_offers_service.postgresql.get_object_models',
        return_value=future([object_model]),
    )

    # act
    result = await offers.get_offers_public(
        request=request,
        realty_user_id=expected_user
    )

    # assert
    assert result == expected_result
    get_offers_by_status_mock.assert_called_once_with(
        status_tab=GetOfferStatusTab.active,
        user_id=expected_user
    )
