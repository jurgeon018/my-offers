from datetime import datetime

import pytest
import pytz
from cian_core.degradation import DegradationResult
from cian_functional_test_utils.helpers import ANY
from cian_test_utils import future
from freezegun import freeze_time
from mock import call
from simple_settings import settings
from simple_settings.utils import settings_stub

from my_offers import enums
from my_offers.entities import AgentHierarchyData, AgentName
from my_offers.entities.enrich import AddressUrlParams
from my_offers.entities.mobile_offer import OfferComplaint
from my_offers.entities.moderation import OfferOffence
from my_offers.entities.offer_view_model import Subagent
from my_offers.enums import DuplicateTabType, ModerationOffenceStatus, OfferStatusTab
from my_offers.repositories.agencies_settings.entities import AgencySettings
from my_offers.repositories.monolith_cian_announcementapi.entities import address_info
from my_offers.repositories.monolith_cian_announcementapi.entities.address_info import AddressInfo, Type
from my_offers.services.offers.enrich.enrich_data import EnrichData, EnrichItem, EnrichParams
from my_offers.services.offers.enrich.load_enrich_data import (
    _load_agency_settings,
    _load_archive_date,
    _load_auctions,
    _load_can_update_edit_dates,
    _load_coverage,
    _load_favorites_counts,
    _load_geo_urls,
    _load_import_errors,
    _load_jk_urls,
    _load_moderation_info,
    _load_moderation_mobile_info,
    _load_offers_payed_by,
    _load_offers_similars_counters,
    _load_payed_till,
    _load_premoderation_info,
    _load_searches_counts,
    _load_subagents,
    _load_views_counts,
    _load_views_daily_counts,
    load_enrich_data,
)


PATH = 'my_offers.services.offers.enrich.load_enrich_data.'


@pytest.mark.gen_test
async def test_load_enrich_data__active_tab(mocker):
    # arrange
    params = EnrichParams(111)
    params.add_similar_offer(11)
    params.add_offer_id(11)
    params.add_jk_id(44)
    params.add_geo_url_id(
        deal_type=enums.DealType.rent,
        offer_type=enums.OfferType.flat,
        geo_type=Type.location,
        geo_id=1,
    )
    load_jk_urls_mock = mocker.patch(
        f'{PATH}_load_jk_urls',
        return_value=future(EnrichItem(key='jk_urls', degraded=False, value={})),
    )
    load_geo_urls_mock = mocker.patch(
        f'{PATH}_load_geo_urls',
        return_value=future(EnrichItem(key='geo_urls', degraded=False, value={})),
    )
    load_can_update_edit_dates_mock = mocker.patch(
        f'{PATH}_load_can_update_edit_dates',
        return_value=future(EnrichItem(key='can_update_edit_dates', degraded=False, value={})),
    )
    load_agency_settings_mock = mocker.patch(
        f'{PATH}_load_agency_settings',
        return_value=future(EnrichItem(key='agency_settings', degraded=False, value=None)),
    )
    load_subagents_mock = mocker.patch(
        f'{PATH}_load_subagents',
        return_value=future(EnrichItem(key='subagents', degraded=False, value=None)),
    )
    load_auctions_mock = mocker.patch(
        f'{PATH}_load_auctions',
        return_value=future(EnrichItem(key='auctions', degraded=False, value={})),
    )
    load_payed_till_mock = mocker.patch(
        f'{PATH}_load_payed_till',
        return_value=future(EnrichItem(key='payed_till', degraded=False, value=None)),
    )
    load_views_counts_mock = mocker.patch(
        f'{PATH}_load_views_counts',
        return_value=future(EnrichItem(key='views_counts', degraded=False, value={})),
    )
    load_searches_counts_mock = mocker.patch(
        f'{PATH}_load_searches_counts',
        return_value=future(EnrichItem(key='searches_counts', degraded=False, value={})),
    )
    load_favorites_counts_mock = mocker.patch(
        f'{PATH}_load_favorites_counts',
        return_value=future(EnrichItem(key='favorites_counts', degraded=False, value={})),
    )
    load_offers_similars_counters_mock = mocker.patch(
        f'{PATH}_load_offers_similars_counters',
        return_value=future(EnrichItem(key='favorites_counts', degraded=False, value={})),
    )
    load_offers_payed_by = mocker.patch(
        f'{PATH}_load_offers_payed_by',
        return_value=future(EnrichItem(key='offers_payed_by', degraded=False, value={})),
    )
    load_offers_payed_by = mocker.patch(
        f'{PATH}_load_offer_relevance_warnings',
        return_value=future(EnrichItem(key='offer_relevance_warnings', degraded=False, value={})),
    )

    expected_data = EnrichData(
        agent_hierarchy_data=AgentHierarchyData(
            is_master_agent=False,
            is_sub_agent=False,
        ),
        auctions={},
        jk_urls={},
        geo_urls={},
        can_update_edit_dates={},
        moderation_info=None,
        import_errors={},
        offers_payed_by={},
        agency_settings=None,
        subagents=None,
        premoderation_info=None,
        archive_date=None,
        payed_till=None,
        offer_relevance_warnings={},
    )
    expected_degradation = {
        'agent_hierarchy_data': True,
        'agency_settings': False,
        'auctions': False,
        'calls_count': True,
        'can_update_edit_dates': False,
        'geo_urls': False,
        'jk_urls': False,
        'subagents': False,
        'payed_till': False,
        'favorites_counts': False,
        'views_counts': False,
        'searches_counts': False,
        'offers_payed_by': False,
        'offer_relevance_warnings': False,
    }

    # act
    data, degradation = await load_enrich_data(params=params, status_tab=OfferStatusTab.active)

    # assert
    assert data == expected_data
    assert degradation == expected_degradation
    load_jk_urls_mock.assert_called_once_with([44])
    load_geo_urls_mock.assert_called_once_with([
        AddressUrlParams(
            deal_type=enums.DealType.rent,
            offer_type=enums.OfferType.flat,
            address_info=[AddressInfo(id=1, type=Type.location)]
        )
    ])
    load_can_update_edit_dates_mock.assert_called_once_with(offer_ids=[11], status_tab=OfferStatusTab.active)
    load_agency_settings_mock.assert_called_once_with(111)
    load_subagents_mock.assert_called_once_with([])
    load_auctions_mock.assert_called_once_with([11])
    load_payed_till_mock.assert_called_once_with([11])
    load_views_counts_mock.assert_called_once_with([11])
    load_searches_counts_mock.assert_called_once_with([11])
    load_favorites_counts_mock.assert_called_once_with([11])
    load_offers_similars_counters_mock.assert_called_once_with(offer_ids=[11], is_test=False)
    load_offers_payed_by.assert_called_once_with([11])


@pytest.mark.gen_test
async def test_load_enrich_data__not_active_tab(mocker):
    # arrange
    params = EnrichParams(111)
    params.add_offer_id(11)
    params.add_jk_id(44)
    params.add_geo_url_id(
        deal_type=enums.DealType.rent,
        offer_type=enums.OfferType.flat,
        geo_type=Type.location,
        geo_id=1,
    )
    load_jk_urls_mock = mocker.patch(
        f'{PATH}_load_jk_urls',
        return_value=future(EnrichItem(key='jk_urls', degraded=False, value={})),
    )
    load_geo_urls_mock = mocker.patch(
        f'{PATH}_load_geo_urls',
        return_value=future(EnrichItem(key='geo_urls', degraded=False, value={})),
    )
    load_can_update_edit_dates_mock = mocker.patch(
        f'{PATH}_load_can_update_edit_dates',
        return_value=future(EnrichItem(key='can_update_edit_dates', degraded=False, value={})),
    )
    load_agency_settings_mock = mocker.patch(
        f'{PATH}_load_agency_settings',
        return_value=future(EnrichItem(key='agency_settings', degraded=False, value=None)),
    )
    load_subagents_mock = mocker.patch(
        f'{PATH}_load_subagents',
        return_value=future(EnrichItem(key='subagents', degraded=False, value=None)),
    )
    load_premoderation_info_mock = mocker.patch(
        f'{PATH}_load_premoderation_info',
        return_value=future(EnrichItem(key='premoderation_info', degraded=False, value=None)),
    )
    load_archive_date_mock = mocker.patch(
        f'{PATH}_load_archive_date',
        return_value=future(EnrichItem(key='archive_date', degraded=False, value=None)),
    )
    load_import_errors_mock = mocker.patch(
        f'{PATH}_load_import_errors',
        return_value=future(EnrichItem(key='import_errors', degraded=False, value={})),
    )
    load_offers_payed_by = mocker.patch(
        f'{PATH}_load_offers_payed_by',
        return_value=future(EnrichItem(key='offers_payed_by', degraded=False, value={})),
    )

    expected_data = EnrichData(
        agent_hierarchy_data=AgentHierarchyData(
            is_master_agent=False,
            is_sub_agent=False,
        ),
        auctions={},
        jk_urls={},
        geo_urls={},
        can_update_edit_dates={},
        import_errors={},
        offers_payed_by={},
        moderation_info=None,
        agency_settings=None,
        subagents=None,
        premoderation_info=None,
        archive_date=None,
        payed_till=None,
    )
    expected_degradation = {
        'agent_hierarchy_data': True,
        'agency_settings': False,
        'can_update_edit_dates': False,
        'geo_urls': False,
        'jk_urls': False,
        'subagents': False,
        'premoderation_info': False,
        'import_errors': False,
        'archive_date': False,
        'offers_payed_by': False
    }

    # act
    data, degradation = await load_enrich_data(params=params, status_tab=OfferStatusTab.not_active)

    # assert
    assert data == expected_data
    assert degradation == expected_degradation
    load_jk_urls_mock.assert_called_once_with([44])
    load_geo_urls_mock.assert_called_once_with([
        AddressUrlParams(
            deal_type=enums.DealType.rent,
            offer_type=enums.OfferType.flat,
            address_info=[AddressInfo(id=1, type=Type.location)]
        )
    ])
    load_can_update_edit_dates_mock.assert_called_once_with(offer_ids=[11], status_tab=OfferStatusTab.not_active)
    load_agency_settings_mock.assert_called_once_with(111)
    load_subagents_mock.assert_called_once_with([])
    load_premoderation_info_mock.assert_called_once_with([11])
    load_import_errors_mock.assert_called_once_with([11])
    load_archive_date_mock.assert_called_once_with([11])
    load_offers_payed_by.assert_called_once_with([11])


@pytest.mark.gen_test
async def test_load_enrich_data__declined_tab(mocker):
    # arrange
    params = EnrichParams(111)
    params.add_offer_id(11)
    params.add_jk_id(44)
    params.add_geo_url_id(
        deal_type=enums.DealType.rent,
        offer_type=enums.OfferType.flat,
        geo_type=Type.location,
        geo_id=1,
    )
    load_jk_urls_mock = mocker.patch(
        f'{PATH}_load_jk_urls',
        return_value=future(EnrichItem(key='jk_urls', degraded=False, value={})),
    )
    load_geo_urls_mock = mocker.patch(
        f'{PATH}_load_geo_urls',
        return_value=future(EnrichItem(key='geo_urls', degraded=False, value={})),
    )
    load_can_update_edit_dates_mock = mocker.patch(
        f'{PATH}_load_can_update_edit_dates',
        return_value=future(EnrichItem(key='can_update_edit_dates', degraded=False, value={})),
    )
    load_agency_settings_mock = mocker.patch(
        f'{PATH}_load_agency_settings',
        return_value=future(EnrichItem(key='agency_settings', degraded=False, value=None)),
    )
    load_subagents_mock = mocker.patch(
        f'{PATH}_load_subagents',
        return_value=future(EnrichItem(key='subagents', degraded=False, value=None)),
    )
    load_moderation_info_mock = mocker.patch(
        f'{PATH}_load_moderation_info',
        return_value=future(EnrichItem(key='moderation_info', degraded=False, value={})),
    )
    load_offers_payed_by = mocker.patch(
        f'{PATH}_load_offers_payed_by',
        return_value=future(EnrichItem(key='offers_payed_by', degraded=False, value={})),
    )

    expected_data = EnrichData(
        agent_hierarchy_data=AgentHierarchyData(
            is_master_agent=False,
            is_sub_agent=False,
        ),
        auctions={},
        jk_urls={},
        geo_urls={},
        can_update_edit_dates={},
        import_errors={},
        moderation_info={},
        offers_payed_by={},
        agency_settings=None,
        subagents=None,
        premoderation_info=None,
        archive_date=None,
        payed_till=None,
    )
    expected_degradation = {
        'agent_hierarchy_data': True,
        'agency_settings': False,
        'can_update_edit_dates': False,
        'geo_urls': False,
        'jk_urls': False,
        'subagents': False,
        'moderation_info': False,
        'offers_payed_by': False
    }

    # act
    data, degradation = await load_enrich_data(params=params, status_tab=OfferStatusTab.declined)

    # assert
    assert data == expected_data
    assert degradation == expected_degradation
    load_jk_urls_mock.assert_called_once_with([44])
    load_geo_urls_mock.assert_called_once_with([
        AddressUrlParams(
            deal_type=enums.DealType.rent,
            offer_type=enums.OfferType.flat,
            address_info=[AddressInfo(id=1, type=Type.location)]
        )
    ])
    load_can_update_edit_dates_mock.assert_called_once_with(offer_ids=[11], status_tab=OfferStatusTab.declined)
    load_agency_settings_mock.assert_called_once_with(111)
    load_subagents_mock.assert_called_once_with([])
    load_moderation_info_mock.assert_called_once_with([11])
    load_offers_payed_by.assert_called_once_with([11])


@pytest.mark.gen_test
@pytest.mark.parametrize('status_tab', [
    OfferStatusTab.deleted,
    OfferStatusTab.archived,
])
async def test_load_enrich_data__tabs_without_enrich(mocker, status_tab):
    # arrange
    params = EnrichParams(111)
    params.add_offer_id(11)
    params.add_jk_id(44)
    params.add_geo_url_id(
        deal_type=enums.DealType.rent,
        offer_type=enums.OfferType.flat,
        geo_type=Type.location,
        geo_id=1,
    )
    load_jk_urls_mock = mocker.patch(
        f'{PATH}_load_jk_urls',
        return_value=future(EnrichItem(key='jk_urls', degraded=False, value={})),
    )
    load_geo_urls_mock = mocker.patch(
        f'{PATH}_load_geo_urls',
        return_value=future(EnrichItem(key='geo_urls', degraded=False, value={})),
    )
    load_can_update_edit_dates_mock = mocker.patch(
        f'{PATH}_load_can_update_edit_dates',
        return_value=future(EnrichItem(key='can_update_edit_dates', degraded=False, value={})),
    )
    load_agency_settings_mock = mocker.patch(
        f'{PATH}_load_agency_settings',
        return_value=future(EnrichItem(key='agency_settings', degraded=False, value=None)),
    )
    load_subagents_mock = mocker.patch(
        f'{PATH}_load_subagents',
        return_value=future(EnrichItem(key='subagents', degraded=False, value=None)),
    )

    load_offers_payed_by = mocker.patch(
        f'{PATH}_load_offers_payed_by',
        return_value=future(EnrichItem(key='offers_payed_by', degraded=False, value={})),
    )

    expected_data = EnrichData(
        agent_hierarchy_data=AgentHierarchyData(
            is_master_agent=False,
            is_sub_agent=False,
        ),
        auctions={},
        jk_urls={},
        geo_urls={},
        can_update_edit_dates={},
        import_errors={},
        offers_payed_by={},
        moderation_info=None,
        agency_settings=None,
        subagents=None,
        premoderation_info=None,
        archive_date=None,
        payed_till=None,
    )
    expected_degradation = {
        'agent_hierarchy_data': True,
        'agency_settings': False,
        'can_update_edit_dates': False,
        'geo_urls': False,
        'jk_urls': False,
        'subagents': False,
        'offers_payed_by': False
    }

    # act
    data, degradation = await load_enrich_data(params=params, status_tab=status_tab)

    # assert
    assert data == expected_data
    assert degradation == expected_degradation
    load_jk_urls_mock.assert_called_once_with([44])
    load_geo_urls_mock.assert_called_once_with([
        AddressUrlParams(
            deal_type=enums.DealType.rent,
            offer_type=enums.OfferType.flat,
            address_info=[AddressInfo(id=1, type=Type.location)]
        )
    ])
    load_can_update_edit_dates_mock.assert_called_once_with(offer_ids=[11], status_tab=status_tab)
    load_agency_settings_mock.assert_called_once_with(111)
    load_subagents_mock.assert_called_once_with([])
    load_offers_payed_by.assert_called_once_with([11])


@pytest.mark.gen_test
async def test_load_enrich_data__empty__empty():
    # arrange
    params = EnrichParams(111)
    expected = EnrichData(
        agent_hierarchy_data=AgentHierarchyData(
            is_master_agent=False,
            is_sub_agent=False,
        ),
        auctions={},
        jk_urls={},
        geo_urls={},
        can_update_edit_dates={},
        import_errors={},
    ), {}

    # act
    result = await load_enrich_data(params=params, status_tab=OfferStatusTab.active)

    # assert
    assert result == expected


@pytest.mark.gen_test
async def test__load_jk_urls(mocker):
    # arrange
    get_newbuilding_urls_degradation_handler_mock = mocker.patch(
        f'{PATH}get_newbuilding_urls_degradation_handler',
        return_value=future(DegradationResult(value={1: 'zz', 2: 'yy'}, degraded=False)),
    )
    excepted = EnrichItem(key='jk_urls', value={1: 'zz', 2: 'yy'}, degraded=False)

    # act
    result = await _load_jk_urls(jk_ids=[1, 2, 3])

    # assert
    assert result == excepted
    get_newbuilding_urls_degradation_handler_mock.assert_called_once_with([1, 2, 3])


@pytest.mark.gen_test
async def test__load_jk_urls__empty__not_called(mocker):
    # arrange
    get_newbuilding_urls_degradation_handler = mocker.patch(
        f'{PATH}get_newbuilding_urls_degradation_handler',
        return_value=future(DegradationResult(value={1: 'zz', 2: 'yy'}, degraded=False)),
    )
    excepted = EnrichItem(key='jk_urls', value={}, degraded=False)

    # act
    result = await _load_jk_urls(jk_ids=[])

    # assert
    assert result == excepted
    get_newbuilding_urls_degradation_handler.assert_not_called()


@pytest.mark.gen_test
async def test__load_geo_urls(mocker):
    # arrange
    params = [
        AddressUrlParams(
            deal_type=enums.DealType.rent,
            offer_type=enums.OfferType.flat,
            address_info=[address_info.AddressInfo()],
        )
    ]

    get_query_strings_for_address_degradation_handler_mock = mocker.patch(
        f'{PATH}get_query_strings_for_address_degradation_handler',
        return_value=future(DegradationResult(value=['aaa'], degraded=False)),
    )

    # act
    result = await _load_geo_urls(params)

    # assert
    assert (enums.DealType.rent, enums.OfferType.flat) in result.value
    get_query_strings_for_address_degradation_handler_mock.assert_called_once_with(
        deal_type=enums.DealType.rent,
        offer_type=enums.OfferType.flat,
        address_elements=[address_info.AddressInfo()],
    )


@pytest.mark.gen_test
async def test__load_geo_urls__degradation__empty(mocker):
    # arrange
    params = [
        AddressUrlParams(
            deal_type=enums.DealType.rent,
            offer_type=enums.OfferType.flat,
            address_info=[address_info.AddressInfo()],
        )
    ]

    get_query_strings_for_address_degradation_handler_mock = mocker.patch(
        f'{PATH}get_query_strings_for_address_degradation_handler',
        return_value=future(DegradationResult(value=[], degraded=True)),
    )

    # act
    result = await _load_geo_urls(params)

    # assert
    assert (enums.DealType.rent, enums.OfferType.flat) not in result.value
    get_query_strings_for_address_degradation_handler_mock.assert_called_once_with(
        deal_type=enums.DealType.rent,
        offer_type=enums.OfferType.flat,
        address_elements=[address_info.AddressInfo()],
    )


@pytest.mark.gen_test
async def test__load_coverage():
    # arrange
    expected = EnrichItem(key='coverage', degraded=True, value={})

    # act
    result = await _load_coverage([11, 22])

    # assert
    assert result == expected


@pytest.mark.gen_test
async def test__load_auctions():
    # arrange
    expected = EnrichItem(key='auctions', degraded=False, value={})

    # act
    result = await _load_auctions([11, 22])

    # assert
    assert result == expected


@pytest.mark.gen_test
async def test__load_can_update_edit_date(mocker):
    # arrange
    can_update_edit_date_degradation_handler_mock = mocker.patch(
        f'{PATH}can_update_edit_date_degradation_handler',
        return_value=future(DegradationResult(value={11: True, 12: False}, degraded=False)),
    )
    expected = EnrichItem(key='can_update_edit_dates', degraded=False, value={11: True, 12: False})

    # act
    result = await _load_can_update_edit_dates([11, 22], status_tab=OfferStatusTab.active)

    # assert
    assert result == expected
    can_update_edit_date_degradation_handler_mock.assert_called_once_with([11, 22])


@pytest.mark.gen_test
async def test__load_moderation_info(mocker):
    # arrange
    offers_ids = [11, 22]
    offer_offence_1 = OfferOffence(
        offence_id=555,
        offence_type=1,
        offence_text='ТЕСТ',
        offence_status=ModerationOffenceStatus.corrected,
        offer_id=11,
        created_by=888,
        created_date=datetime(2020, 1, 1),
        row_version=0,
        updated_at=datetime(2020, 1, 1),
        created_at=datetime(2020, 1, 1),
    )
    offer_offence_2 = OfferOffence(
        offence_id=555,
        offence_type=1,
        offence_text='ТЕСТ',
        offence_status=ModerationOffenceStatus.corrected,
        offer_id=22,
        created_by=888,
        created_date=datetime(2020, 1, 1),
        row_version=0,
        updated_at=datetime(2020, 1, 1),
        created_at=datetime(2020, 1, 1),
    )

    expected = EnrichItem(
        key='moderation_info',
        degraded=False,
        value={11: offer_offence_1, 22: offer_offence_2}
    )
    get_offer_offence_mock = mocker.patch(
        f'{PATH}get_offers_offence_degradation_handler',
        return_value=future(DegradationResult(value=[offer_offence_1, offer_offence_2], degraded=False))
    )

    # act
    result = await _load_moderation_info(offers_ids)

    # assert
    assert result == expected
    get_offer_offence_mock.assert_has_calls([
        call(offer_ids=[11, 22], status=ModerationOffenceStatus.confirmed)
    ])


@pytest.mark.gen_test
async def test__load_import_errors(mocker):
    # arrange
    get_last_import_errors_mock = mocker.patch(
        f'{PATH}get_last_import_errors_degradation_handler',
        return_value=future(DegradationResult(value={11: 'zzz'}, degraded=False))
    )
    expected = EnrichItem(key='import_errors', degraded=False, value={11: 'zzz'})

    # act
    result = await _load_import_errors([11])

    # assert
    assert result == expected
    get_last_import_errors_mock.assert_called_once_with([11])


@pytest.mark.gen_test
async def test__load_agency_settings(mocker):
    # arrange
    get_master_user_id_mock = mocker.patch(
        f'{PATH}get_master_user_id',
        return_value=future(22)
    )

    get_settings_degradation_handler_mock = mocker.patch(
        f'{PATH}get_settings_degradation_handler',
        return_value=future(DegradationResult(
            value=AgencySettings(
                can_sub_agents_edit_offers_from_xml=False,
                can_sub_agents_publish_offers=False,
                can_sub_agents_view_agency_balance=False,
                display_all_agency_offers=False,
            ),
            degraded=False,
        ))
    )

    expected = EnrichItem(
        key='agency_settings',
        degraded=False,
        value=AgencySettings(
            can_sub_agents_edit_offers_from_xml=False,
            can_sub_agents_publish_offers=False,
            can_sub_agents_view_agency_balance=False,
            display_all_agency_offers=False,
        )
    )

    # act
    result = await _load_agency_settings(11)

    # assert
    assert result == expected
    get_master_user_id_mock.assert_called_once_with(11)
    get_settings_degradation_handler_mock.assert_called_once_with(22)


@pytest.mark.gen_test
async def test__load_agency_settings__no_ma__empty(mocker):
    # arrange
    get_master_user_id_mock = mocker.patch(
        f'{PATH}get_master_user_id',
        return_value=future()
    )

    get_settings_degradation_handler_mock = mocker.patch(
        f'{PATH}get_settings_degradation_handler',
        return_value=future(DegradationResult(
            value=AgencySettings(
                can_sub_agents_edit_offers_from_xml=False,
                can_sub_agents_publish_offers=False,
                can_sub_agents_view_agency_balance=False,
                display_all_agency_offers=False,
            ),
            degraded=False,
        ))
    )

    expected = EnrichItem(
        key='agency_settings',
        degraded=False,
        value=None,
    )

    # act
    result = await _load_agency_settings(11)

    # assert
    assert result == expected
    get_master_user_id_mock.assert_called_once_with(11)
    get_settings_degradation_handler_mock.assert_not_called()


@pytest.mark.gen_test
async def test__load_subagents(mocker):
    # arrange
    get_agent_names_mock = mocker.patch(
        f'{PATH}get_agent_names_degradation_handler',
        return_value=future(DegradationResult(
            value=[
                AgentName(id=12, first_name='Zz', last_name='Yy', middle_name='Mm'),
                AgentName(id=14, first_name=None, last_name=None, middle_name=None),
            ],
            degraded=False,
        ))
    )
    expected = EnrichItem(key='subagents', value={12: Subagent(id=12, name='Zz Yy')}, degraded=False)

    # act
    result = await _load_subagents([1, 2])

    # assert
    assert result == expected
    get_agent_names_mock.assert_called_once_with([1, 2])


@pytest.mark.gen_test
async def test__load_subagents__empty__empty(mocker):
    # arrange
    get_agent_names_mock = mocker.patch(
        f'{PATH}get_agent_names_degradation_handler',
        return_value=future(DegradationResult(
            value=[
                AgentName(id=12, first_name='Zz', last_name='Yy', middle_name='Mm'),
                AgentName(id=14, first_name=None, last_name=None, middle_name=None),
            ],
            degraded=False,
        ))
    )
    expected = EnrichItem(key='subagents', value=None, degraded=False)

    # act
    result = await _load_subagents([])

    # assert
    assert result == expected
    get_agent_names_mock.assert_not_called()


@pytest.mark.gen_test
async def test__load_premoderation_info(mocker):
    # arrange
    expected = EnrichItem(key='premoderation_info', value={11}, degraded=False)

    get_offer_premoderations_mock = mocker.patch(
        f'{PATH}get_offer_premoderations_degradation_handler',
        return_value=future(DegradationResult(value=[11], degraded=False))
    )

    # act
    result = await _load_premoderation_info([11, 22])

    # assert
    assert result == expected

    get_offer_premoderations_mock.assert_called_once_with([11, 22])


@pytest.mark.gen_test
async def test__load_archive_date(mocker):
    # arrange
    get_offers_update_at_mock = mocker.patch(
        f'{PATH}get_offers_update_at_degradation_handler',
        return_value=future(DegradationResult(value={1: datetime(2020, 3, 30)}, degraded=False))
    )
    expected = EnrichItem(key='archive_date', value={1: datetime(2020, 3, 30)}, degraded=False)

    # act
    result = await _load_archive_date([1])

    # assert
    assert result == expected
    get_offers_update_at_mock.assert_called_once_with([1])


@pytest.mark.gen_test
async def test__load_payed_till(mocker):
    # arrange
    get_offers_payed_till_mock = mocker.patch(
        f'{PATH}get_offers_payed_till_excluding_calltracking_degradation_handler',
        return_value=future(DegradationResult(value={1: datetime(2020, 3, 30)}, degraded=False))
    )
    expected = EnrichItem(key='payed_till', value={1: datetime(2020, 3, 30)}, degraded=False)

    # act
    result = await _load_payed_till([1])

    # assert
    assert result == expected
    get_offers_payed_till_mock.assert_called_once_with([1])


async def test__load_views_counts(mocker):
    # arrange
    offer_ids = [1, 2, 3]
    date_to = datetime(2020, 4, 20, tzinfo=pytz.utc)
    date_from = datetime(2020, 4, 10, tzinfo=pytz.utc)

    get_views_counts_mock = mocker.patch(
        f'{PATH}get_views_counts_degradation_handler',
        return_value=future(DegradationResult(value={1: 1, 2: 2, 3: 3}, degraded=False))
    )
    expected = EnrichItem(key='views_counts', value={1: 1, 2: 2, 3: 3}, degraded=False)

    # act
    with freeze_time(date_to):
        result = await _load_views_counts(
            offer_ids=offer_ids
        )

    # assert
    assert result == expected
    get_views_counts_mock.assert_called_once_with(
        offer_ids=offer_ids,
        date_from=date_from,
        date_to=date_to
    )


async def test_load_views_daily_counts(mocker):
    # arrange
    offer_ids = [1, 2, 3]
    date = datetime(2020, 4, 10, tzinfo=pytz.utc)

    get_views_counts_mock = mocker.patch(
        f'{PATH}get_views_current_degradation_handler',
        return_value=future(DegradationResult(value={1: 1, 2: 2, 3: 3}, degraded=False))
    )
    expected = EnrichItem(key='views_daily_counts', value={1: 1, 2: 2, 3: 3}, degraded=False)

    # act
    with freeze_time(date):
        result = await _load_views_daily_counts(offer_ids)

    # assert
    assert result == expected
    get_views_counts_mock.assert_called_once_with(
        offer_ids=offer_ids,
        date=date,
    )


async def test_load_moderation_mobile_info(mocker):
    # arrange
    offer_ids = [1, 2]

    load_moderation_mobile_info_mock = mocker.patch(
        f'{PATH}get_offers_offence_degradation_handler',
        return_value=future(
            DegradationResult(
                value=[OfferOffence(
                    offence_id=1833685,
                    created_date=ANY,
                    created_by=14037408,
                    offer_id=209194477,
                    offence_type=1,
                    offence_status=ModerationOffenceStatus.confirmed,
                    offence_text='Тестовое удаление Тестовое удаление',
                    row_version=20038084139,
                    created_at=ANY,
                    updated_at=ANY
                ),
                    OfferOffence(
                        offence_id=1833685,
                        created_date=ANY,
                        created_by=14037408,
                        offer_id=209194477,
                        offence_type=55,
                        offence_status=ModerationOffenceStatus.confirmed,
                        offence_text='Тестовое удаление Тестовое удаление',
                        row_version=20038084139,
                        created_at=ANY,
                        updated_at=ANY
                    )],
                degraded=False,
            )
        )
    )
    expected = EnrichItem(
        key='moderation_info',
        value={
            209194477: [
                OfferComplaint(id=1833685, date=ANY, comment='Тестовое удаление Тестовое удаление'),
                OfferComplaint(id=1833685, date=ANY, comment='Тестовое удаление Тестовое удаление'),
            ]
        },
        degraded=False,
    )

    # act
    result = await _load_moderation_mobile_info(
        offer_ids=offer_ids
    )

    # assert
    assert result == expected
    load_moderation_mobile_info_mock.assert_called_once_with(
        offer_ids=offer_ids,
        status=ModerationOffenceStatus.confirmed,
    )


async def test__load_searches_counts(mocker):
    # arrange
    offer_ids = [1, 2, 3]
    date_to = datetime(2020, 4, 20, tzinfo=pytz.utc)
    date_from = datetime(2020, 4, 10, tzinfo=pytz.utc)

    get_searches_counts_mock = mocker.patch(
        f'{PATH}get_searches_counts_degradation_handler',
        return_value=future(DegradationResult(value={1: 1, 2: 2, 3: 3}, degraded=False))
    )
    expected = EnrichItem(key='searches_counts', value={1: 1, 2: 2, 3: 3}, degraded=False)

    # act
    with freeze_time(date_to):
        result = await _load_searches_counts(
            offer_ids=offer_ids
        )

    # assert
    assert result == expected
    get_searches_counts_mock.assert_called_once_with(
        offer_ids=offer_ids,
        date_from=date_from,
        date_to=date_to
    )


async def test__load_favorites_counts(mocker):
    # arrange
    offer_ids = [1, 2, 3]

    get_favorites_counts_mock = mocker.patch(
        f'{PATH}get_favorites_counts_degradation_handler',
        return_value=future(DegradationResult(value={1: 1, 2: 2, 3: 3}, degraded=False))
    )
    expected = EnrichItem(key='favorites_counts', value={1: 1, 2: 2, 3: 3}, degraded=False)

    # act
    with settings_stub(FAVORITES_FROM_MCS=False):
        result = await _load_favorites_counts(
            offer_ids=offer_ids
        )

    # assert
    assert result == expected
    get_favorites_counts_mock.assert_called_once_with(
        offer_ids=offer_ids,
    )


async def test__load_offers_similars_counters__offers_ids_is_empty(mocker):
    # arrange
    offer_ids = []
    expected = EnrichItem(key='offers_similars_counts', degraded=False, value={})

    get_similars_counters_by_offer_ids_mock = mocker.patch(
        f'{PATH}get_similars_counters_by_offer_ids_degradation_handler',
    )

    # act
    result = await _load_offers_similars_counters(
        offer_ids=offer_ids,
        is_test=True
    )

    # assert
    assert result == expected
    get_similars_counters_by_offer_ids_mock.assert_not_called()


async def test__load_offers_similars_counters__degraded(mocker):
    # arrange
    offer_ids = [1, 2, 3]
    expected = EnrichItem(key='offers_similars_counts', degraded=True, value={})

    get_similars_counters_by_offer_ids_mock = mocker.patch(
        f'{PATH}get_similars_counters_by_offer_ids_degradation_handler',
        return_value=future(DegradationResult(value={}, degraded=True))
    )

    # act
    result = await _load_offers_similars_counters(
        offer_ids=offer_ids,
        is_test=True
    )

    # assert
    assert result == expected
    get_similars_counters_by_offer_ids_mock.assert_called_once_with(
        offer_ids=offer_ids,
        price_kf=settings.SIMILAR_PRICE_KF,
        room_delta=settings.SIMILAR_ROOM_DELTA,
        suffix='test',
        tab_type=DuplicateTabType.all
    )


async def test_load_offers_payed_by(mocker):
    # arrange
    offer_ids = [1, ]
    expected = {1: None}

    get_offers_payed_by_degradation_handler = mocker.patch(
        f'{PATH}get_offers_payed_by_degradation_handler',
        return_value=future(DegradationResult(value=expected, degraded=False))
    )

    # act
    result = await _load_offers_payed_by(offer_ids)

    # assert
    get_offers_payed_by_degradation_handler.assert_called_once_with(
        offer_ids
    )
    assert result.value == expected
    assert not result.degraded
