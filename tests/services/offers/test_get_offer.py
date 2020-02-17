from datetime import datetime

import pytest
from cian_test_utils import future

from my_offers.entities import GetOffersRequest
from my_offers.entities.get_offers import (
    Filter,
    GetOffer,
    GetOffersPrivateRequest,
    GetOffersResponse,
    OfferCounters,
    PageInfo,
    Pagination,
    Statistics,
)
from my_offers.entities.offer_view_model import OfferGeo, PriceInfo
from my_offers.enums import GetOfferStatusTab
from my_offers.repositories.monolith_cian_announcementapi.entities import BargainTerms, ObjectModel, Phone
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category
from my_offers.services import offers
from my_offers.services.offers import get_offers_private
from my_offers.services.offers.get_offers_service import _get_pagination


@pytest.mark.gen_test
async def test_get_offer(mocker):
    # arrange
    expected_user = 777
    request = GetOffersRequest(
        filters=Filter(
            status_tab=GetOfferStatusTab.active,
            sort_type=None,
            deal_type=None,
            offer_type=None,
            services=None,
            sub_agent_ids=None,
            has_photo=None,
            is_manual=None,
            is_in_hidden_base=None,
            search_text=None,
        ),
        pagination=None,
        sort=None,
    )
    object_model = ObjectModel(
        id=111,
        bargain_terms=BargainTerms(price=123),
        category=Category.flat_rent,
        phones=[Phone(country_code='1', number='12312')],
        creation_date=datetime(2020, 2, 11, 17, 00),
    )
    expected_result = GetOffersResponse(
        offers=[
            GetOffer(
                main_photo_url=None,
                title='',
                url='https://cian.ru/rent/flat/111',
                geo=OfferGeo(address=None, newbuilding=None, underground=None),
                subagent=None,
                price_info=PriceInfo(exact=None, range=None),
                features=[],
                publish_features=None,
                vas=[],
                is_from_package=False,
                is_manual=False,
                is_publication_time_ends=False,
                created_at=datetime(2020, 2, 11, 17, 00),
                id=111,
                statistics=Statistics(),
                auction=None
            )
        ],
        counters=OfferCounters(active=1, not_active=0, declined=0, archived=0),
        page=PageInfo(count=1, page_count=1, can_load_more=False),
    )

    get_offers_by_status_mock = mocker.patch(
        'my_offers.services.offers.get_offers_service.postgresql.get_object_models',
        return_value=future(([object_model], 1)),
    )

    # act
    result = await offers.get_offers_public(
        request=request,
        realty_user_id=expected_user
    )

    # assert
    assert result == expected_result
    get_offers_by_status_mock.assert_called_once_with(
        filters={'status_tab': 'active', 'master_user_id': 777},
        limit=20,
        offset=0,
    )


@pytest.mark.gen_test
async def test_get_offers_private(mocker):
    # arrange
    request = GetOffersPrivateRequest(
        user_id=111,
        filters=Filter(
            status_tab=GetOfferStatusTab.active,
            sort_type=None,
            deal_type=None,
            offer_type=None,
            services=None,
            sub_agent_ids=None,
            has_photo=None,
            is_manual=None,
            is_in_hidden_base=None,
            search_text=None,
        ),
        pagination=None,
        sort=None,
    )

    response = mocker.sentinel.response

    get_offers_public_mock = mocker.patch(
        'my_offers.services.offers.get_offers_service.get_offers_public',
        return_value=future(response),
    )

    # act
    result = await get_offers_private(request)

    # assert
    assert result == response
    get_offers_public_mock.assert_called_once_with(
        request=request,
        realty_user_id=111,
    )


@pytest.mark.parametrize(
    ('pagination', 'expected'),
    (
        (None, (20, 0)),
        (Pagination(limit=40, page=None, offset=None), (40, 0)),
        (Pagination(limit=40, page=None, offset=20), (40, 20)),
        (Pagination(limit=40, page=2, offset=None), (40, 40)),
        (Pagination(limit=40, page=3, offset=55), (40, 55)),
    )
)
def test__get_pagination(pagination, expected):
    # arrange

    # act
    result = _get_pagination(pagination)

    # assert
    assert result == expected
