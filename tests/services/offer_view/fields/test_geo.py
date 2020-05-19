import pytest

from my_offers.entities import MobileOfferGeo
from my_offers.entities.duplicates import MobileUnderground
from my_offers.entities.offer_view_model import Address, Newbuilding, OfferGeo, Underground
from my_offers.enums.offer_address import AddressType
from my_offers.repositories.monolith_cian_announcementapi.entities import AddressInfo, Geo, Jk, UndergroundInfo
from my_offers.repositories.monolith_cian_announcementapi.entities.address_info import Type
from my_offers.services.offer_view.fields.geo import (
    _get_address,
    _get_address_for_mobile,
    _get_newbuilding,
    _get_underground,
    _get_underground_for_mobile,
    prepare_geo,
    prepare_geo_for_mobile,
)
from my_offers.services.offers.enrich.enrich_data import AddressUrls


PATH = 'my_offers.services.offer_view.fields.geo.'


def test_prepare_geo(mocker):
    # arrange
    urls = AddressUrls()
    address_info = AddressInfo()
    underground_info = UndergroundInfo()
    jk = Jk()

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

    get_address_mock = mocker.patch(f'{PATH}_get_address', return_value=[address])
    get_newbuilding_mock = mocker.patch(f'{PATH}_get_newbuilding', return_value=newbuilding)
    get_underground_mock = mocker.patch(f'{PATH}_get_underground', return_value=underground)

    # act

    result = prepare_geo(
        geo=Geo(address=[address_info], undergrounds=[underground_info], jk=jk),
        geo_urls=urls,
        jk_urls={},
    )

    # assert
    assert result == expected

    get_address_mock.assert_called_once_with(address_info=[address_info], urls=urls)
    get_newbuilding_mock.assert_called_once_with(jk=jk, urls={})
    get_underground_mock.assert_called_once_with(
        undergrounds_info=[underground_info],
        address_info=[address_info],
        urls=urls,
    )


def test_prepare_geo__not_geo__empty(mocker):
    # arrange
    urls = AddressUrls()

    newbuilding = Newbuilding(name='zz', search_url='yy')
    address = Address(name='aa', search_url='bb', type=AddressType.location)
    underground = Underground(
        region_id=1,
        line_color='red',
        name='MM',
        search_url='ss',
    )

    expected = OfferGeo()

    get_address_mock = mocker.patch(f'{PATH}_get_address', return_value=[address])
    get_newbuilding_mock = mocker.patch(f'{PATH}_get_newbuilding', return_value=newbuilding)
    get_underground_mock = mocker.patch(f'{PATH}_get_underground', return_value=underground)

    # act
    result = prepare_geo(
        geo=None,
        geo_urls=urls,
        jk_urls={},
    )

    # assert
    assert result == expected

    get_address_mock.assert_not_called()
    get_newbuilding_mock.assert_not_called()
    get_underground_mock.assert_not_called()


def test__get_address(mocker):
    # arrange
    address_info = [AddressInfo(full_name='aa', type=Type.location)]
    expected = [Address(name='aa', search_url='bb', type=AddressType.location)]
    address_urls = AddressUrls()
    address_urls.add_url(address=address_info[0], url='bb')

    # act
    result = _get_address(address_info=address_info, urls=address_urls)

    # assert
    assert result == expected


def test__get_address__no_adress__none(mocker):
    # arrange
    address_info = None
    address_urls = AddressUrls()

    # act
    result = _get_address(address_info=address_info, urls=address_urls)

    # assert
    assert result is None


@pytest.mark.parametrize(
    ('undergrounds_info', 'address_info', 'expected'),
    (
        (None, None, None),
        (None, [AddressInfo()], None),
        ([UndergroundInfo()], None, None),
        ([UndergroundInfo()], [AddressInfo()], None),
        ([UndergroundInfo(is_default=True)], [AddressInfo()], None),
    ),
)
def test__get_underground(mocker, undergrounds_info, address_info, expected):
    # arrange & act
    result = _get_underground(
        undergrounds_info=undergrounds_info,
        address_info=address_info,
        urls=AddressUrls(),
    )

    # assert
    assert result == expected


@pytest.mark.parametrize(
    ('jk', 'urls', 'expected'),
    (
        (None, {}, None),
        (Jk(id=22, name='yy'), {22: 'bb'}, Newbuilding(name='ЖК "yy"', search_url='bb')),
    ),
)
def test__get_newbuilding(mocker, jk, urls, expected):
    # arrange & act
    result = _get_newbuilding(jk=jk, urls=urls)

    # assert
    assert result == expected


def test_prepare_geo_for_mobile__empty_geo__empty():
    # arrange & act
    result = prepare_geo_for_mobile(Geo())

    # assert
    assert result == MobileOfferGeo(address=[], underground=None)


def test__get_address_for_mobile__empty_address_info__empty():
    # arrange & act
    result = _get_address_for_mobile([])

    # assert
    assert result == []


@pytest.mark.parametrize(
    ('undergrounds', 'addresses', 'expected'),
    (
        ([], [], None),
        ([UndergroundInfo(is_default=True)], [], None),
        ([UndergroundInfo(is_default=True)], [AddressInfo()], None),
        (
            [UndergroundInfo(is_default=True, line_color='red', name='ZZZ')],
            [AddressInfo(type=Type.location, id=77)],
            MobileUnderground(region_id=77, line_color='red', name='ZZZ')
        ),
    )
)
def test__get_underground_for_mobile(undergrounds, addresses, expected):
    # arrange & act
    result = _get_underground_for_mobile(undergrounds=undergrounds, addresses=addresses)

    # assert
    assert result == expected
