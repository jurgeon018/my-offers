import pytest
from cian_test_utils import future

from my_offers.enums import DealType, OfferType
from my_offers.repositories.monolith_cian_announcementapi.entities import AddressInfo
from my_offers.repositories.monolith_cian_announcementapi.entities.address_info import Type
from my_offers.repositories.monolith_python.entities import (
    InternalApiSerializeToQueryStringsResponse,
    SerializeToQueryStringsRequest,
    SerializeToQueryStringsResponse,
)
from my_offers.repositories.monolith_python.entities.serialize_to_query_strings_response import Status
from my_offers.services.seo_urls.get_seo_urls import (
    _get_query_params_for_address_element,
    _make_query_params,
    get_query_strings_for_address,
)


@pytest.mark.gen_test
async def test_get_query_strings_for_address(mocker):
    # arrange
    get_region_ids_cached_mock = mocker.patch(
        'my_offers.services.seo_urls.get_seo_urls.get_region_ids_cached',
        return_value=future([1, 2, 3]),
    )
    get_query_params_for_address_element_mock = mocker.patch(
        'my_offers.services.seo_urls.get_seo_urls._get_query_params_for_address_element',
        side_effect=[{'q': 1}, {'q': 2}],
    )
    internal_api_serialize_query_params_mock = mocker.patch(
        'my_offers.services.seo_urls.get_seo_urls.internal_api_serialize_query_params',
        return_value=future(SerializeToQueryStringsResponse(
            data=InternalApiSerializeToQueryStringsResponse(
                query_strings=['asd1', 'asd2']
            ),
            status=Status.ok,
        )),
    )

    # act
    result = await get_query_strings_for_address(
        address_elements=[AddressInfo(id=1), AddressInfo(id=2)],
        deal_type=DealType.sale,
        offer_type=OfferType.flat,
    )

    # assert
    assert result == ['https://cian.ru/cat.php?asd1', 'https://cian.ru/cat.php?asd2']
    get_region_ids_cached_mock.assert_called_once_with()
    get_query_params_for_address_element_mock.assert_has_calls([
        mocker.call(
            address_element=AddressInfo(id=1),
            query_params={'offer_type': 'flat', 'deal_type': 'sale'},
            region_ids=[1, 2, 3],
            deal_type=DealType.sale,
        ),
        mocker.call(
            address_element=AddressInfo(id=2),
            query_params={'offer_type': 'flat', 'deal_type': 'sale'},
            region_ids=[1, 2, 3],
            deal_type=DealType.sale,
        ),
    ])
    internal_api_serialize_query_params_mock.assert_called_once_with(
        SerializeToQueryStringsRequest(query_params=[{'q': 1}, {'q': 2}]),
    )


def test_get_query_params_for_address_element(mocker):
    # arrange
    make_query_params_mock = mocker.patch(
        'my_offers.services.seo_urls.get_seo_urls._make_query_params',
        return_value={'asd': 'zxc'},
    )
    query_params = {'query': 'params'}

    # act
    result = _get_query_params_for_address_element(
        address_element=AddressInfo(id=1),
        query_params=query_params,
        region_ids={1},
        deal_type=DealType.sale,
    )

    # assert
    assert result == {
        'query': 'params',
        'asd': 'zxc',
    }
    assert query_params == {'query': 'params'}
    make_query_params_mock.assert_called_once_with(
        address_element=AddressInfo(id=1),
        region_ids={1},
        skip_foot=True,
    )


def test_get_query_params_for_address_element__rent(mocker):
    # arrange
    make_query_params_mock = mocker.patch(
        'my_offers.services.seo_urls.get_seo_urls._make_query_params',
        return_value={'asd': 'zxc'},
    )

    # act
    result = _get_query_params_for_address_element(
        address_element=AddressInfo(id=1),
        query_params={'query': 'params'},
        region_ids={1},
        deal_type=DealType.rent,
    )

    # assert
    assert result == {
        'query': 'params',
        'asd': 'zxc',
    }
    make_query_params_mock.assert_called_once_with(
        address_element=AddressInfo(id=1),
        region_ids={1},
        skip_foot=False,
    )


@pytest.mark.parametrize(
    'address_element,region_ids,skip_foot,expected',
    [
        (
            AddressInfo(id=10, type=Type.underground),
            {},
            False,
            {'foot_min': 25, 'only_foot': '2', 'locations': [{'metro': 10}], 'engine_version': 2},
        ),
        (AddressInfo(id=10, type=Type.underground), {}, True, {'locations': [{'metro': 10}], 'engine_version': 2}),
        (AddressInfo(id=10, type=Type.location), {}, True, {'locations': [{'location': 10}], 'engine_version': 2}),
        (AddressInfo(id=10, type=Type.location), {10}, True, {'region': [{'location': 10}], 'engine_version': 2}),
    ]
)
def test_make_query_params(address_element, region_ids, skip_foot, expected):
    # act
    result = _make_query_params(address_element=address_element, region_ids=region_ids, skip_foot=skip_foot)

    # assert
    assert result == expected
