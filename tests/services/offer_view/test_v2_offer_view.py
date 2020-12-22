import pytest

from my_offers.entities import AgentHierarchyData
from my_offers.entities.available_actions import AvailableActions
from my_offers.entities.get_offers import ActiveInfo, GetOfferV2, PageSpecificInfo, Statistics
from my_offers.entities.offer_view_model import OfferGeo, PriceInfo
from my_offers.enums import OfferPayedByType
from my_offers.repositories.monolith_cian_announcementapi.entities import BargainTerms, ObjectModel, Phone
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category, Status
from my_offers.services.offer_view import v2_build_offer_view
from my_offers.services.offers.enrich.enrich_data import EnrichData


@pytest.fixture(name='enrich_data_mock')
def enrich_data_fixture():
    return EnrichData(
        auctions={},
        jk_urls={},
        geo_urls={},
        can_update_edit_dates={},
        import_errors={},
    )


@pytest.fixture(name='enrich_data_with_offers_payed_by_mock')
def enrich_data_with_offers_payed_by_fixture():
    return EnrichData(
        auctions={},
        jk_urls={},
        geo_urls={},
        can_update_edit_dates={},
        import_errors={},
        offers_payed_by={
            1: OfferPayedByType.by_agent,
            2: OfferPayedByType.by_master,
            3: None
            }
    )


def test_build_offer_view(enrich_data_mock):
    # arrange
    raw_offer = ObjectModel(
        id=111,
        cian_id=111,
        status=Status.published,
        bargain_terms=BargainTerms(price=123),
        category=Category.flat_rent,
        phones=[Phone(country_code='1', number='12312')]
    )
    expected_result = GetOfferV2(
        id=111,
        main_photo_url=None,
        title='',
        url='https://cian.ru/rent/flat/111',
        geo=OfferGeo(address=None, newbuilding=None, underground=None),
        subagent=None,
        price_info=PriceInfo(exact=None, range=None),
        features=[],
        is_manual=True,
        display_date=None,
        archived_at=None,
        status='Опубликовано',
        statistics=Statistics(shows=None, views=None, favorites=None),
        available_actions=AvailableActions(
            can_edit=True,
            can_restore=False,
            can_update_edit_date=False,
            can_move_to_archive=True,
            can_delete=True,
            can_raise=True,
            can_raise_without_addform=False,
            can_change_publisher=True,
            can_view_similar_offers=True
        ),
        page_specific_info=PageSpecificInfo(
            active_info=ActiveInfo(
                vas=[],
                is_from_package=False,
                is_publication_time_ends=False,
                publish_features=[],
                auction=None,
                payed_till=None,
            ),
            not_active_info=None,
            declined_info=None
        ),
        status_type=None,
        payed_by=None
    )
    agent_hierarchy_data = AgentHierarchyData(
        is_master_agent=True,
        is_sub_agent=False,
    )

    # act
    result = v2_build_offer_view(
        agent_hierarchy_data=agent_hierarchy_data,
        object_model=raw_offer,
        enrich_data=enrich_data_mock
    )

    # assert
    assert result == expected_result


@pytest.mark.parametrize('offer_id_from_mock, expected_available_actions', [
     (
        1, AvailableActions(
             can_update_edit_date=False,
             can_move_to_archive=False,
             can_delete=False,
             can_edit=False,
             can_restore=False,
             can_raise=False,
             can_raise_without_addform=False,
             can_change_publisher=False,
             can_view_similar_offers=False
            ),
     ), (
         2, AvailableActions(
             can_edit=True,
             can_restore=False,
             can_update_edit_date=False,
             can_move_to_archive=True,
             can_delete=True,
             can_raise=True,
             can_raise_without_addform=False,
             can_change_publisher=True,
             can_view_similar_offers=True
            ),
     ), (
         3, AvailableActions(
             can_edit=True,
             can_restore=False,
             can_update_edit_date=False,
             can_move_to_archive=True,
             can_delete=True,
             can_raise=True,
             can_raise_without_addform=False,
             can_change_publisher=True,
             can_view_similar_offers=True
             )
     ),
])
def test_build_offer_view_depends_on_payed_by(
        enrich_data_with_offers_payed_by_mock,
        offer_id_from_mock,
        expected_available_actions
):
    # arrange
    raw_offer = ObjectModel(
        id=offer_id_from_mock,
        cian_id=offer_id_from_mock,
        status=Status.published,
        bargain_terms=BargainTerms(price=123),
        category=Category.flat_rent,
        phones=[Phone(country_code='1', number='12312')]
    )
    expected_result = GetOfferV2(
        id=offer_id_from_mock,
        main_photo_url=None,
        title='',
        url=f'https://cian.ru/rent/flat/{offer_id_from_mock}',
        geo=OfferGeo(address=None, newbuilding=None, underground=None),
        subagent=None,
        price_info=PriceInfo(exact=None, range=None),
        features=[],
        is_manual=True,
        display_date=None,
        archived_at=None,
        status='Опубликовано',
        statistics=Statistics(shows=None, views=None, favorites=None),
        available_actions=expected_available_actions,
        page_specific_info=PageSpecificInfo(
            active_info=ActiveInfo(
                vas=[],
                is_from_package=False,
                is_publication_time_ends=False,
                publish_features=[],
                auction=None,
                payed_till=None,
            ),
            not_active_info=None,
            declined_info=None
        ),
        status_type=None,
        payed_by=enrich_data_with_offers_payed_by_mock.offers_payed_by.get(offer_id_from_mock)
    )
    agent_hierarchy_data = AgentHierarchyData(
        is_master_agent=True,
        is_sub_agent=False,
    )

    # act
    result = v2_build_offer_view(
        agent_hierarchy_data=agent_hierarchy_data,
        object_model=raw_offer,
        enrich_data=enrich_data_with_offers_payed_by_mock
    )

    # assert
    assert result == expected_result
