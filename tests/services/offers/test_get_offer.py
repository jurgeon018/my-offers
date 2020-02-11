import pytest
from cian_test_utils import future

from my_offers.entities import GetOffersRequest
from my_offers.entities.get_offers import GetOffer, GetOffersResponse, OfferCounters
from my_offers.entities.offer_view_model import OfferGeo, PriceInfo
from my_offers.enums import GetOfferStatusTab
from my_offers.repositories.monolith_cian_announcementapi.entities import BargainTerms, ObjectModel, Phone
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category
from my_offers.services import offers


@pytest.mark.gen_test
async def test_get_offer(mocker):
    # arrange
    user_id = 666
    request = GetOffersRequest(
        status_tab=GetOfferStatusTab.active
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
            is_from_import=False,
            is_publication_time_ends=False,
            created_at=None,
            id=None,
            statistics=None,
            auction=None
        )],
        counters=OfferCounters(active=1, not_active=0, declined=0, archived=0))

    get_offers_by_status_mock = mocker.patch(
        'my_offers.services.offers.get_offers_service.postgresql.get_offers_by_status',
        return_value=future([object_model]),
    )

    # act
    result = await offers.get_offers(
        request=request,
        realty_user_id=user_id
    )

    # assert
    assert result == expected_result
    get_offers_by_status_mock.assert_called_once_with(
        status_tab=GetOfferStatusTab.active,
        user_id=user_id
    )


@pytest.mark.gen_test
async def test_get_offer__realty_user_id_is_none(mocker):
    # arrange
    user_id = None
    request = GetOffersRequest(
        status_tab=GetOfferStatusTab.active
    )

    # act
    with pytest.raises(Exception) as e:
        await offers.get_offers(
            request=request,
            realty_user_id=user_id
        )

    # assert
    assert e.value.args[0] == 'Не указан X-Real-UserId'
