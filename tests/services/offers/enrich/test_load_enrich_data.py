import pytest
from cian_core.degradation import DegradationResult
from cian_test_utils import future

from my_offers import enums
from my_offers.entities.enrich import AddressUrlParams
from my_offers.repositories.monolith_cian_announcementapi.entities import address_info
from my_offers.repositories.monolith_cian_announcementapi.entities.address_info import AddressInfo, Type
from my_offers.services.offers.enrich.enrich_data import EnrichData, EnrichItem, EnrichParams
from my_offers.services.offers.enrich.load_enrich_data import (
    _load_auctions,
    _load_can_update_edit_dates,
    _load_geo_urls,
    _load_jk_urls,
    _load_statistic,
    load_enrich_data,
)


PATH = 'my_offers.services.offers.enrich.load_enrich_data.'


@pytest.mark.gen_test
async def test_load_enrich_data(mocker):
    # arrange
    params = EnrichParams()
    params.add_offer_id(11)
    params.add_jk_id(44)
    params.add_geo_url_id(
        deal_type=enums.DealType.rent,
        offer_type=enums.OfferType.flat,
        geo_type=Type.location,
        geo_id=1,
    )

    load_statistic_mock = mocker.patch(
        f'{PATH}_load_statistic',
        return_value=future(EnrichItem(key='statistics', degraded=False, value={})),
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

    expected = (
        EnrichData(statistics={}, auctions={}, jk_urls={}, geo_urls={}, can_update_edit_dates={}, import_errors={},),
        {
            'auctions': False,
            'can_update_edit_dates': False,
            'geo_urls': False,
            'jk_urls': False,
            'statistics': False,
            'import_errors': False,
        }
    )

    # act
    result = await load_enrich_data(params)

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


@pytest.mark.gen_test
async def test_load_enrich_data__empty__empty(mocker):
    # arrange
    params = EnrichParams()
    expected = EnrichData(
        statistics={},
        auctions={},
        jk_urls={},
        geo_urls={},
        can_update_edit_dates={},
        import_errors={},
    ), {}

    # act
    result = await load_enrich_data(params)

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
async def test__load_statistic(mocker):
    # arrange
    expected = EnrichItem(key='statistics', degraded=False, value={})

    # act
    result = await _load_statistic([11, 22])

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
