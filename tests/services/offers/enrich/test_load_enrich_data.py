import pytest
from cian_core.degradation import DegradationResult
from cian_test_utils import future

from my_offers import enums
from my_offers.entities.enrich import AddressUrlParams
from my_offers.repositories.monolith_cian_announcementapi.entities import address_info
from my_offers.services.offers.enrich.load_enrich_data import _load_geo_urls, _load_jk_urls


PATH = 'my_offers.services.offers.enrich.load_enrich_data.'


@pytest.mark.gen_test
async def test__load_jk_urls(mocker):
    # arrange
    get_newbuilding_urls_degradation_handler = mocker.patch(
        f'{PATH}get_newbuilding_urls_degradation_handler',
        return_value=future(DegradationResult(value={1: 'zz', 2: 'yy'}, degraded=False)),
    )

    # act
    result = await _load_jk_urls(jk_ids=[1, 2, 3])

    # assert
    assert result == {1: 'zz', 2: 'yy'}
    get_newbuilding_urls_degradation_handler.assert_called_once_with([1, 2, 3])


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
    assert (enums.DealType.rent, enums.OfferType.flat) in result
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
    assert (enums.DealType.rent, enums.OfferType.flat) not in result
    get_query_strings_for_address_degradation_handler_mock.assert_called_once_with(
        deal_type=enums.DealType.rent,
        offer_type=enums.OfferType.flat,
        address_elements=[address_info.AddressInfo()],
    )
