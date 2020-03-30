from datetime import datetime

import pytest
from cian_core.degradation import DegradationResult
from cian_test_utils import future
from mock import call

from my_offers import enums
from my_offers.entities import AgentName
from my_offers.entities.enrich import AddressUrlParams
from my_offers.entities.moderation import OfferOffence
from my_offers.entities.offer_view_model import Subagent
from my_offers.enums import ModerationOffenceStatus
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
    _load_geo_urls,
    _load_import_errors,
    _load_jk_urls,
    _load_moderation_info,
    _load_premoderation_info,
    _load_subagents,
    load_enrich_data,
)


PATH = 'my_offers.services.offers.enrich.load_enrich_data.'


@pytest.mark.gen_test
async def test_load_enrich_data(mocker):
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

    load_statistic_mock = mocker.patch(
        f'{PATH}_load_coverage',
        return_value=future(EnrichItem(key='coverage', degraded=False, value={})),
    )
    load_auctions_mock = mocker.patch(
        f'{PATH}_load_auctions',
        return_value=future(EnrichItem(key='auctions', degraded=False, value={})),
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
    load_import_errors_mock = mocker.patch(
        f'{PATH}_load_import_errors',
        return_value=future(EnrichItem(key='import_errors', degraded=False, value={})),
    )
    load_moderation_info_mock = mocker.patch(
        f'{PATH}_load_moderation_info',
        return_value=future(EnrichItem(key='moderation_info', degraded=False, value={})),
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

    expected = (
        EnrichData(
            coverage={},
            auctions={},
            jk_urls={},
            geo_urls={},
            can_update_edit_dates={},
            moderation_info={},
            import_errors={},
            agency_settings=None,
            subagents=None,
            premoderation_info=None,
            archive_date=None,
        ),
        {
            'agency_settings': False,
            'auctions': False,
            'can_update_edit_dates': False,
            'geo_urls': False,
            'jk_urls': False,
            'coverage': False,
            'import_errors': False,
            'moderation_info': False,
            'subagents': False,
            'premoderation_info': False,
            'archive_date': False,
        }
    )

    # act
    result = await load_enrich_data(params=params)

    # assert
    assert result == expected
    load_statistic_mock.assert_called_once_with([11])
    load_auctions_mock.assert_called_once_with([11])
    load_jk_urls_mock.assert_called_once_with([44])
    load_geo_urls_mock.assert_called_once_with([
        AddressUrlParams(
            deal_type=enums.DealType.rent,
            offer_type=enums.OfferType.flat,
            address_info=[AddressInfo(id=1, type=Type.location)]
        )
    ])
    load_can_update_edit_dates_mock.assert_called_once_with([11])
    load_import_errors_mock.assert_called_once_with([11])
    load_moderation_info_mock.assert_called_once_with([11])
    load_agency_settings_mock.assert_called_once_with(111)
    load_subagents_mock.assert_called_once_with([])
    load_premoderation_info_mock.assert_called_once_with([11])
    load_archive_date_mock.assert_called_once_with([11])


@pytest.mark.gen_test
async def test_load_enrich_data__empty__empty(mocker):
    # arrange
    params = EnrichParams(111)
    expected = EnrichData(
        coverage={},
        auctions={},
        jk_urls={},
        geo_urls={},
        can_update_edit_dates={},
        import_errors={},
    ), {}

    # act
    result = await load_enrich_data(params=params)

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
async def test__load_coverage(mocker):
    # arrange
    expected = EnrichItem(key='coverage', degraded=True, value={})

    # act
    result = await _load_coverage([11, 22])

    # assert
    assert result == expected


@pytest.mark.gen_test
async def test__load_auctions(mocker):
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
    result = await _load_can_update_edit_dates([11, 22])

    # assert
    assert result == expected
    can_update_edit_date_degradation_handler_mock.assert_called_once_with([11, 22])


@pytest.mark.gen_test
async def test___load_moderation_info(mocker):
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
        updated_at=None,
        created_at=None,
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
        updated_at=None,
        created_at=None,
    )

    expected = EnrichItem(
        key='moderation_info',
        degraded=False,
        value={11: offer_offence_1, 22: offer_offence_2}
    )
    get_offer_offence_mock = mocker.patch(
        f'{PATH}postgresql.get_offers_offence',
        return_value=future([offer_offence_1, offer_offence_2])
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
        f'{PATH}get_last_import_errors',
        return_value=future({11: 'zzz'})
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
        f'{PATH}get_agent_names',
        return_value=future([
            AgentName(id=12, first_name='Zz', last_name='Yy', middle_name='Mm'),
            AgentName(id=14, first_name=None, last_name=None, middle_name=None),
        ])
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
        f'{PATH}get_agent_names',
        return_value=future([
            AgentName(id=12, first_name='Zz', last_name='Yy', middle_name='Mm'),
            AgentName(id=14, first_name=None, last_name=None, middle_name=None),
        ])
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
        f'{PATH}get_offer_premoderations',
        return_value=future([11])
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
        f'{PATH}get_offers_update_at',
        return_value=future({1: datetime(2020, 3, 30)})
    )
    expected = EnrichItem(key='archive_date', value={1: datetime(2020, 3, 30)}, degraded=False)

    # act
    result = await _load_archive_date([1])

    # assert
    assert result == expected
    get_offers_update_at_mock.assert_called_once_with([1])
