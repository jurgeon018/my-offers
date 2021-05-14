from datetime import datetime

import pytest
from cian_helpers.timezone import TIMEZONE
from cian_test_utils import future

from my_offers.entities import AgentHierarchyData, GetOffersPrivateRequest
from my_offers.entities.available_actions import AvailableActions
from my_offers.entities.get_offers import ActiveInfo, Filter, GetOfferV2, PageSpecificInfo, Statistics
from my_offers.entities.offer_view_model import OfferGeo, PriceInfo
from my_offers.enums import OfferStatusTab
from my_offers.repositories.monolith_cian_announcementapi.entities import BargainTerms, ObjectModel, Phone
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category, Status
from my_offers.services.offers import get_offer_views, v2_get_offers_private
from my_offers.services.offers.enrich.enrich_data import EnrichData


PATH = 'my_offers.services.offers._v2_get_offers.'


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
        'my_offers.services.offers._get_offers.load_enrich_data',
        return_value=future((
            EnrichData(
                agent_hierarchy_data=AgentHierarchyData(
                    is_master_agent=False,
                    is_sub_agent=False,
                ),
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
        cian_id=111,
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
                url='https://cian.ru/rent/flat/111/',
                geo=OfferGeo(address=None, newbuilding=None, underground=None),
                subagent=None,
                price_info=PriceInfo(exact=None, range=None),
                features=[],
                is_manual=True,
                display_date=TIMEZONE.localize(datetime(2020, 2, 11, 17, 0)),
                id=111,
                archived_at=None,
                status='Опубликовано',
                available_actions=AvailableActions(
                    can_edit=True,
                    can_restore=False,
                    can_update_edit_date=False,
                    can_move_to_archive=True,
                    can_delete=True,
                    can_raise=True,
                    can_raise_without_addform=False,
                    can_change_publisher=False,
                    can_view_similar_offers=True
                ),
                statistics=Statistics(shows=None, views=None, favorites=None),
                page_specific_info=PageSpecificInfo(
                    active_info=ActiveInfo(
                        vas=[],
                        is_from_package=False,
                        is_publication_time_ends=False,
                        publish_features=[],
                        auction=None
                    ),
                ),
                status_type=None,
                payed_by=None,
                multiposting=None
            )
        ],
        {}
    )

    # act
    result = await get_offer_views(
        object_models=[object_model],
        user_id=777,
        status_tab=OfferStatusTab.active
    )

    # assert
    assert result == expected
    load_enrich_data_mock.assert_called_once()
