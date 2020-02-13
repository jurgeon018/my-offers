import pytest
from cian_test_utils import future

from my_offers.entities.get_offers import GetOffer, Statistics
from my_offers.entities.offer_view_model import Address, Newbuilding, OfferGeo, PriceInfo, Underground
from my_offers.enums.offer_address import AddressType
from my_offers.repositories.monolith_cian_announcementapi.entities import (
    AddressInfo,
    BargainTerms,
    Geo,
    Jk,
    ObjectModel,
    Phone,
    Photo,
    PublishTerm,
    PublishTerms,
    TariffIdentificator,
    UndergroundInfo,
)
from my_offers.repositories.monolith_cian_announcementapi.entities.address_info import Type as RealtyAddressType
from my_offers.repositories.monolith_cian_announcementapi.entities.bargain_terms import SaleType
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category, Source
from my_offers.repositories.monolith_cian_announcementapi.entities.publish_term import Services
from my_offers.repositories.monolith_cian_announcementapi.entities.tariff_identificator import TariffGridType
from my_offers.services.offer_view.offer_view import build_offer_view


@pytest.mark.gen_test
async def test_build_offer_view():
    # arrange
    raw_offer = ObjectModel(
        bargain_terms=BargainTerms(price=123),
        category=Category.building_rent,
        phones=[
            Phone(country_code='1', number='12312')
        ]
    )
    expected_result = GetOffer(
        main_photo_url=None,
        title=None,
        url=None,
        geo=OfferGeo(address=None, newbuilding=None, underground=None),
        subagent=None,
        price_info=PriceInfo(exact='123 ₽/мес.'),
        features=[],
        publish_features=None,
        vas=None,
        is_from_package=False,
        is_manual=False,
        is_publication_time_ends=False,
        created_at=None,
        id=None,
        statistics=Statistics(),
        auction=None,
    )

    # act
    result = await build_offer_view(object_model=raw_offer)

    # assert
    assert result == expected_result


@pytest.mark.gen_test
@pytest.mark.parametrize('photos, expected', [
    ([Photo(mini_url='http://photo_url.ru/1_mini.jpg')], 'http://photo_url.ru/1_mini.jpg'),
    ([Photo(mini_url=None)], None),
    ([], None),
    (None, None),
])
async def test_build_offer_view__main_photo_url(photos, expected):
    # arrange
    raw_offer = ObjectModel(
        bargain_terms=BargainTerms(price=123),
        category=Category.building_rent,
        phones=[
            Phone(country_code='1', number='12312')
        ],
        photos=photos
    )

    # act
    result = await build_offer_view(object_model=raw_offer)

    # assert
    assert result.main_photo_url == expected


@pytest.mark.gen_test
async def test_build_offer_view__subagent():
    # arrange
    raw_offer = ObjectModel(
        bargain_terms=BargainTerms(price=123),
        category=Category.building_rent,
        phones=[
            Phone(country_code='1', number='12312')
        ]
    )

    # act
    result = await build_offer_view(object_model=raw_offer)

    # assert
    assert result.subagent is None


@pytest.mark.gen_test
@pytest.mark.parametrize('source, is_manual', [
    (Source.upload, True),
    (Source.website, False),
    (Source.mobile_app, False),
])
async def test_build_offer_view__is__from_import(source, is_manual):
    # arrange
    raw_offer = ObjectModel(
        source=source,
        bargain_terms=BargainTerms(price=123),
        category=Category.building_rent,
        phones=[
            Phone(country_code='1', number='12312')
        ]
    )

    # act
    result = await build_offer_view(object_model=raw_offer)

    # assert
    assert result.is_manual is is_manual


@pytest.mark.gen_test
@pytest.mark.parametrize('deal_type, expected', [
    (Category.bed_rent, '123 ₽/мес.'),
    (Category.building_sale, '123 ₽'),
])
async def test_build_offer_view__price_info(deal_type, expected):
    # arrange
    raw_offer = ObjectModel(
        bargain_terms=BargainTerms(price=123.0),
        category=deal_type,
        phones=[
            Phone(country_code='1', number='12312')
        ]
    )

    # act
    result = await build_offer_view(object_model=raw_offer)

    # assert
    assert result.price_info == PriceInfo(exact=expected)


@pytest.mark.gen_test
@pytest.mark.parametrize('deal_type, prepared, expected', [
    (Category.flat_sale, dict(mortgage_allowed=True), ['Возможна ипотека']),
    (
        Category.flat_sale,
        dict(mortgage_allowed=True, sale_type=SaleType.free),
        ['Возможна ипотека', 'Свободная продажа']
    ),

    (Category.bed_rent, dict(agent_fee=50), ['Агенту: 50%']),
    (Category.bed_rent, dict(agent_fee=50, client_fee=10), ['Агенту: 50%', 'Клиенту: 10%']),
    (
        Category.bed_rent,
        dict(agent_fee=50, client_fee=10, deposit=1000),
        ['Агенту: 50%', 'Клиенту: 10%', 'Залог: 1000 ₽']
    ),
])
async def test_build_offer_view__features(deal_type, prepared, expected):
    # arrange
    raw_offer = ObjectModel(
        bargain_terms=BargainTerms(price=123.0, **prepared),
        category=deal_type,
        phones=[Phone(country_code='1', number='12312')]
    )

    # act
    result = await build_offer_view(object_model=raw_offer)

    # assert
    assert result.features == expected


@pytest.mark.gen_test
@pytest.mark.parametrize('publish_terms, expected', [
    (PublishTerms(autoprolong=True), ['автопродление']),
    (PublishTerms(autoprolong=True, terms=[PublishTerm(days=10)]), ['автопродление', 'осталось 10 д.']),
])
async def test_build_offer_view__publish_features(publish_terms, expected):
    # arrange
    raw_offer = ObjectModel(
        bargain_terms=BargainTerms(price=123.0),
        publish_terms=publish_terms,
        category=Category.bed_rent,
        phones=[Phone(country_code='1', number='12312')]
    )

    # act
    result = await build_offer_view(object_model=raw_offer)

    # assert
    assert result.publish_features == expected


@pytest.mark.gen_test
@pytest.mark.parametrize('terms, expected', [
    (
        [PublishTerm(services=[Services.calltracking, Services.paid])],
        [Services.calltracking, Services.paid]
    ),
    (
        [PublishTerm(services=[Services.calltracking, Services.paid]), PublishTerm(services=[Services.top3])],
        [Services.calltracking, Services.paid, Services.top3]
    ),
])
async def test_build_offer_view__vas(terms, expected):
    # arrange
    raw_offer = ObjectModel(
        bargain_terms=BargainTerms(price=123.0),
        publish_terms=PublishTerms(terms=terms),
        category=Category.bed_rent,
        phones=[Phone(country_code='1', number='12312')]
    )

    # act
    result = await build_offer_view(object_model=raw_offer)

    # assert
    assert result.vas == expected


@pytest.mark.gen_test
@pytest.mark.parametrize('publish_terms, expected', [
    (None, False),
    (PublishTerms(terms=[]), False),
    (PublishTerms(terms=[]), False),
    (PublishTerms(terms=[PublishTerm(tariff_identificator=None)]), False),
    (PublishTerms(terms=[PublishTerm(tariff_identificator=TariffIdentificator())]), False),
    (
        PublishTerms(terms=[PublishTerm(tariff_identificator=TariffIdentificator(
            tariff_grid_type=TariffGridType.package_tariff))]),
        False
    ),
    (
        PublishTerms(terms=[PublishTerm(tariff_identificator=TariffIdentificator(
            tariff_grid_type=TariffGridType.service_package))]),
        True
    )
])
async def test_build_offer_view__is_from_package(publish_terms, expected):
    # arrange
    raw_offer = ObjectModel(
        bargain_terms=BargainTerms(price=123.0),
        publish_terms=publish_terms,
        category=Category.bed_rent,
        phones=[Phone(country_code='1', number='12312')]
    )

    # act
    result = await build_offer_view(object_model=raw_offer)

    # assert
    assert result.is_from_package is expected


@pytest.mark.gen_test
async def test_build_offer_view__is_publication_time_ends():
    # arrange
    raw_offer = ObjectModel(
        bargain_terms=BargainTerms(price=123.0),
        category=Category.bed_rent,
        phones=[Phone(country_code='1', number='12312')]
    )

    # act
    result = await build_offer_view(object_model=raw_offer)

    # assert
    assert result.is_publication_time_ends is False


@pytest.mark.gen_test
@pytest.mark.parametrize('geo, expected', [
    (None, None),
    (Geo(undergrounds=[], address=[]), None),
    (
        Geo(
            undergrounds=[UndergroundInfo(line_color='#12321', name='Сокольники', is_default=True)],
            address=[AddressInfo(id=1, type=AddressType.location)]
        ),
        Underground(search_url='', region_id=1, line_color='#12321', name='Сокольники')
    )
])
async def test_build_offer_view__geo_underground(mocker, geo, expected):
    # arrange
    raw_offer = ObjectModel(
        bargain_terms=BargainTerms(price=123.0),
        category=Category.bed_rent,
        phones=[Phone(country_code='1', number='12312')],
        geo=geo,
    )

    prepare_geo_mock = mocker.patch(
        'my_offers.services.offer_view.offer_view.prepare_geo',
        return_value=future(OfferGeo())
    )

    # act
    await build_offer_view(object_model=raw_offer)

    # assert
    prepare_geo_mock.assert_called_once()


@pytest.mark.gen_test
@pytest.mark.parametrize('geo, expected', [
    (None, None),
    (Geo(jk=Jk(name='Lol kek')), Newbuilding(search_url='', name='Lol kek'))
])
async def test_build_offer_view__newbuilding(geo, expected):
    # arrange
    raw_offer = ObjectModel(
        bargain_terms=BargainTerms(price=123.0),
        category=Category.bed_rent,
        phones=[Phone(country_code='1', number='12312')],
        geo=geo
    )

    # act
    result = await build_offer_view(object_model=raw_offer)

    # assert
    assert result.geo.newbuilding == expected
