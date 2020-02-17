import pytest
from cian_test_utils import future

from my_offers import enums
from my_offers.entities.offer_view_model import Address, Newbuilding, OfferGeo, Underground
from my_offers.enums.offer_address import AddressType
from my_offers.repositories.monolith_cian_announcementapi.entities import AddressInfo, Geo, Jk, UndergroundInfo
from my_offers.repositories.monolith_cian_announcementapi.entities.address_info import Type
from my_offers.services.offer_view.fields.geo import _get_address, _get_newbuilding, _get_underground, prepare_geo


PATH = 'my_offers.services.offer_view.geo.'


@pytest.mark.gen_test
async def test_prepare_geo(mocker):
    # arrange
    address_info = AddressInfo()
    underground_info = UndergroundInfo()
    jk = Jk()
    deal_type = enums.DealType.sale
    offer_type = enums.OfferType.flat

    newbuilding = Newbuilding(name='zz', search_url='yy')
    address = Address(name='aa', search_url='bb', type=AddressType.location)
    underground = Underground(
        region_id=1,
        line_color='red',
        name='MM',
        search_url='ss',
    )

    expected = OfferGeo(
        address=[address],
        newbuilding=newbuilding,
        underground=underground,

    )

    get_address_mock = mocker.patch(f'{PATH}_get_address', return_value=future([address]))
    get_newbuilding_mock = mocker.patch(f'{PATH}_get_newbuilding', return_value=future(newbuilding))
    get_underground_mock = mocker.patch(f'{PATH}_get_underground', return_value=future(underground))

    # act
    result = await prepare_geo(
        geo=Geo(address=[address_info], undergrounds=[underground_info], jk=jk),
        deal_type=deal_type,
        offer_type=offer_type,
    )

    # assert
    assert result == expected

    get_address_mock.assert_called_once_with(address_info=[address_info], deal_type=deal_type, offer_type=offer_type)
    get_newbuilding_mock.assert_called_once_with(jk)
    get_underground_mock.assert_called_once_with(
        undergrounds_info=[underground_info],
        address_info=[address_info],
        deal_type=deal_type,
        offer_type=offer_type,
    )


@pytest.mark.gen_test
async def test_prepare_geo__not_geo__empty(mocker):
    # arrange
    deal_type = enums.DealType.sale
    offer_type = enums.OfferType.flat

    newbuilding = Newbuilding(name='zz', search_url='yy')
    address = Address(name='aa', search_url='bb', type=AddressType.location)
    underground = Underground(
        region_id=1,
        line_color='red',
        name='MM',
        search_url='ss',
    )

    expected = OfferGeo()

    get_address_mock = mocker.patch(f'{PATH}_get_address', return_value=future([address]))
    get_newbuilding_mock = mocker.patch(f'{PATH}_get_newbuilding', return_value=future(newbuilding))
    get_underground_mock = mocker.patch(f'{PATH}_get_underground', return_value=future(underground))

    # act
    result = await prepare_geo(
        geo=None,
        deal_type=deal_type,
        offer_type=offer_type,
    )

    # assert
    assert result == expected

    get_address_mock.assert_not_called()
    get_newbuilding_mock.assert_not_called()
    get_underground_mock.assert_not_called()


@pytest.mark.gen_test
async def test__get_address(mocker):
    # arrange
    address_info = [AddressInfo(full_name='aa', type=Type.location)]
    deal_type = enums.DealType.sale
    offer_type = enums.OfferType.flat

    expected = [Address(name='aa', search_url='bb', type=AddressType.location)]
    get_query_strings_for_address_mock = mocker.patch(
        f'{PATH}get_query_strings_for_address',
        return_value=future(['bb'])
    )

    # act
    result = await _get_address(address_info=address_info, deal_type=deal_type, offer_type=offer_type)

    # assert
    assert result == expected
    get_query_strings_for_address_mock.assert_called_once_with(
        address_elements=address_info,
        deal_type=deal_type,
        offer_type=offer_type,
    )


@pytest.mark.gen_test
async def test__get_address__no_adress__none(mocker):
    # arrange
    address_info = None
    deal_type = enums.DealType.sale
    offer_type = enums.OfferType.flat

    get_query_strings_for_address_mock = mocker.patch(
        f'{PATH}get_query_strings_for_address',
        return_value=future(['bb'])
    )

    # act
    result = await _get_address(address_info=address_info, deal_type=deal_type, offer_type=offer_type)

    # assert
    assert result is None
    get_query_strings_for_address_mock.assert_not_called()


@pytest.mark.gen_test
@pytest.mark.parametrize(
    ('undergrounds_info', 'address_info', 'expected'),
    (
        (None, None, None),
        (None, [AddressInfo()], None),
        ([UndergroundInfo()], None, None),
        ([UndergroundInfo()], [AddressInfo()], None),
        ([UndergroundInfo(is_default=True)], [AddressInfo()], None),
        (
            [UndergroundInfo(id=11, name='xx', line_color='red', is_default=True)],
            [AddressInfo(id=22, type=Type.location)],
            Underground(
                search_url='bb',
                region_id=22,
                line_color='red',
                name='xx',
            )
        ),
    ),
)
async def test__get_underground(mocker, undergrounds_info, address_info, expected):
    # arrange
    deal_type = enums.DealType.sale
    offer_type = enums.OfferType.flat
    mocker.patch(f'{PATH}get_query_strings_for_address', return_value=future(['bb']))

    # act
    result = await _get_underground(
        undergrounds_info=undergrounds_info,
        address_info=address_info,
        deal_type=deal_type,
        offer_type=offer_type,
    )

    # assert
    assert result == expected


@pytest.mark.gen_test
@pytest.mark.parametrize(
    ('jk', 'expected'),
    (
        (None, None),
        (Jk(id=22, name='yy'), Newbuilding(name='yy', search_url='bb')),
    ),
)
async def test__get_newbuilding(mocker, jk, expected):
    # arrange
    mocker.patch(f'{PATH}get_newbuilding_url_cached', return_value=future('bb'))

    # act
    result = await _get_newbuilding(jk)

    # assert
    assert result == expected
