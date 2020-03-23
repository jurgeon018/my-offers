from datetime import datetime

import pytest
from cian_test_utils import future

from my_offers.entities import GetOffersPrivateRequest
from my_offers.entities.get_offers import (
    ActiveInfo,
    AvailableActions,
    Filter,
    GetOffersRequest,
    GetOffersV2Response,
    GetOfferV2,
    OfferCounters,
    PageInfo,
    PageSpecificInfo,
    Statistics,
)
from my_offers.entities.offer_view_model import OfferGeo, PriceInfo
from my_offers.enums import GetOffersSortType, OfferStatusTab
from my_offers.repositories.monolith_cian_announcementapi.entities import BargainTerms, ObjectModel, Phone
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category, Status
from my_offers.services.offers import v2_get_offer_views, v2_get_offers_private, v2_get_offers_public
from my_offers.services.offers.enrich.enrich_data import EnrichData


PATH = 'my_offers.services.offers._v2_get_offers.'


@pytest.mark.gen_test
async def test_v2_get_offers_public(mocker):
    # arrange
    expected_user = 777
    request = GetOffersRequest(
        filters=Filter(
            status_tab=OfferStatusTab.active,
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

    get_offer = GetOfferV2(
        main_photo_url=None,
        title='',
        url='https://cian.ru/rent/flat/111',
        geo=OfferGeo(address=None, newbuilding=None, underground=None),
        subagent=None,
        price_info=PriceInfo(exact=None, range=None),
        features=[],
        is_manual=False,
        created_at=datetime(2020, 2, 11, 17, 00),
        id=111,
        statistics=Statistics(),
        archived_at=None,
        status=None,
        available_actions=AvailableActions(can_update_edit_date=False, can_move_to_archive=False, can_delete=False),
        page_specific_info=PageSpecificInfo(),
    )

    expected_result = GetOffersV2Response(
        offers=[get_offer],
        counters=OfferCounters(active=1, not_active=2, declined=3, archived=4),
        page=PageInfo(count=1, page_count=1, can_load_more=False),
        degradation={},
    )

    get_offers_by_status_mock = mocker.patch(
        f'{PATH}postgresql.get_object_models',
        return_value=future(([object_model], 1)),
    )

    get_offer_views_mock = mocker.patch(
        f'{PATH}v2_get_offer_views',
        return_value=future(([get_offer], {})),
    )
    get_offer_counters_mock = mocker.patch(
        f'{PATH}get_offer_counters',
        return_value=future(OfferCounters(active=1, not_active=2, declined=3, archived=4)),
    )

    get_filters_mock = mocker.patch(
        f'{PATH}get_filters',
        return_value=future({'status_tab': 'active', 'master_user_id': [777]}),
    )

    # act
    result = await v2_get_offers_public(
        request=request,
        realty_user_id=expected_user
    )

    # assert
    assert result == expected_result
    get_offer_views_mock.assert_called_once_with(object_models=[object_model])
    get_offers_by_status_mock.assert_called_once_with(
        filters={'status_tab': 'active', 'master_user_id': [777]},
        limit=20,
        offset=0,
        sort_type=GetOffersSortType.by_default,
    )
    get_offer_counters_mock.assert_called_once_with({'status_tab': 'active', 'master_user_id': [777]})
    get_filters_mock.assert_called_once_with(
        filters=Filter(
            status_tab=OfferStatusTab.active,
            deal_type=None,
            offer_type=None,
            services=None,
            sub_agent_ids=None,
            has_photo=None,
            is_manual=None,
            is_in_hidden_base=None,
            search_text=None,
        ),
        user_id=777,
    )


@pytest.mark.gen_test
async def test_v2_get_offers_private(mocker):
    # arrange
    request = GetOffersPrivateRequest(
        user_id=111,
        filters=Filter(
            status_tab=OfferStatusTab.active,
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
        f'{PATH}v2_get_offers_public',
        return_value=future(response),
    )

    # act
    result = await v2_get_offers_private(request)

    # assert
    assert result == response
    get_offers_public_mock.assert_called_once_with(
        request=request,
        realty_user_id=111,
    )


@pytest.mark.gen_test
async def test_v2_get_offer_views(mocker):
    # arrange
    load_enrich_data_mock = mocker.patch(
        f'{PATH}load_enrich_data',
        return_value=future((
            EnrichData(
                coverage={},
                auctions={},
                jk_urls={},
                geo_urls={},
                can_update_edit_dates={},
                import_errors={},
            ),
            {}
        )),
    )

    object_model = ObjectModel(
        id=111,
        bargain_terms=BargainTerms(price=123),
        category=Category.flat_rent,
        phones=[Phone(country_code='1', number='12312')],
        creation_date=datetime(2020, 2, 11, 17, 00),
        status=Status.published,
    )

    expected = (
        [
            GetOfferV2(
                main_photo_url=None,
                title='',
                url='https://cian.ru/rent/flat/111',
                geo=OfferGeo(address=None, newbuilding=None, underground=None),
                subagent=None,
                price_info=PriceInfo(exact=None, range=None),
                features=[],
                is_manual=False,
                created_at=datetime(2020, 2, 11, 17, 0),
                id=111,
                archived_at=None,
                status='Опубликовано',
                available_actions=AvailableActions(
                    can_update_edit_date=False,
                    can_move_to_archive=False,
                    can_delete=True
                ),
                statistics=Statistics(shows=None, views=None, favorites=None),
                page_specific_info=PageSpecificInfo(
                    active_info=ActiveInfo(
                        vas=[],
                        is_from_package=False,
                        is_autoprolong=False,
                        is_publication_time_ends=False,
                        publish_features=[],
                        auction=None
                    ),
                )
            )
        ],
        {}
    )

    # act
    result = await v2_get_offer_views(object_models=[object_model])

    # assert
    assert result == expected
    load_enrich_data_mock.assert_called_once()
