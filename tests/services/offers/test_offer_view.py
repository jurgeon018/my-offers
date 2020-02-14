import pytest

from my_offers.entities.get_offers import GetOffer, Statistics
from my_offers.entities.offer_view_model import Address, Newbuilding, OfferGeo, PriceInfo, Underground
from my_offers.enums.offer_address import AddressType
from my_offers.repositories.monolith_cian_announcementapi.entities import (
    AddressInfo,
    BargainTerms,
    Building,
    Geo,
    Jk,
    Land,
    ObjectModel,
    Phone,
    Photo,
    PublishTerm,
    PublishTerms,
    TariffIdentificator,
    UndergroundInfo,
)
from my_offers.repositories.monolith_cian_announcementapi.entities.address_info import Type as RealtyAddressType
from my_offers.repositories.monolith_cian_announcementapi.entities.bargain_terms import (
    Currency,
    LeaseType,
    PriceType,
    SaleType,
)
from my_offers.repositories.monolith_cian_announcementapi.entities.land import AreaUnitType
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category, Source
from my_offers.repositories.monolith_cian_announcementapi.entities.publish_term import Services
from my_offers.repositories.monolith_cian_announcementapi.entities.tariff_identificator import TariffGridType
from my_offers.services.offers.offer_view import build_offer_view


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
        title='',
        url=None,
        geo=OfferGeo(address=None, newbuilding=None, underground=None),
        subagent=None,
        price_info=PriceInfo(exact=None, range=None),
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
    result = build_offer_view(object_model=raw_offer)

    # assert
    assert result == expected_result


@pytest.mark.gen_test
@pytest.mark.parametrize('category, prepared, building, expected', [
    (
        Category.building_rent,
        dict(rooms_count=1, total_area=60.0, floor_number=3), Building(floors_count=19),
        '1-комн. кв., 60 м2, 3/19 этаж'
    ),
    (
        Category.building_rent,
        dict(rooms_count=1, total_area=60.0, floor_number=3, is_apartments=True), Building(floors_count=19),
        '1-комн. апарт., 60 м2, 3/19 этаж'
    ),
    (
        Category.building_rent,
        dict(rooms_count=8, total_area=60.0, floor_number=3), Building(floors_count=19),
        'многокомн. кв., 60 м2, 3/19 этаж'
    ),
    (
        Category.office_rent,
        dict(total_area=60.0, min_area=10.0, can_parts=True), None,
        'Свободное назначение, от 10 до 60 м²'
    ),
])
async def test_build_offer_view__tittle(category, prepared, building, expected):
    # arrange
    raw_offer = ObjectModel(
        bargain_terms=BargainTerms(price=123),
        category=category,
        phones=[Phone(country_code='1', number='12312')],
        building=building,
        **prepared
    )

    # act
    result = build_offer_view(object_model=raw_offer)

    # assert
    assert result.title == expected


@pytest.mark.gen_test
@pytest.mark.parametrize('category, land, expected', [
    (
        Category.land_sale,
        Land(area=16.57, area_unit_type=AreaUnitType.sotka),
        'участок 16.57 сот.'
    ),
    (
        Category.land_sale,
        Land(area=16.57, area_unit_type=AreaUnitType.hectare),
        'участок 16.57 га.'
    ),

])
async def test_build_offer_view__tittle__land(category, land, expected):
    # arrange
    raw_offer = ObjectModel(
        bargain_terms=BargainTerms(price=123),
        category=category,
        phones=[Phone(country_code='1', number='12312')],
        land=land
    )

    # act
    result = build_offer_view(object_model=raw_offer)

    # assert
    assert result.title == expected


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
    result = build_offer_view(object_model=raw_offer)

    # assert
    assert result.main_photo_url == expected


@pytest.mark.gen_test
@pytest.mark.parametrize('category, expected', [
    (Category.room_rent, f'http://cian.ru/rent/flat/123'),
    (Category.office_rent, f'http://cian.ru/rent/commercial/123'),
    (Category.house_rent, f'http://cian.ru/rent/suburban/123'),
    (Category.new_building_flat_sale, f'http://cian.ru/sale/flat/123'),
])
async def test_build_offer_view__offer_url(category, expected):
    # arrange
    raw_offer = ObjectModel(
        id=123,
        bargain_terms=BargainTerms(price=123),
        category=category,
        phones=[Phone(country_code='1', number='12312')],
    )

    # act
    result = build_offer_view(object_model=raw_offer)

    # assert
    assert result.url == expected


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
    result = build_offer_view(object_model=raw_offer)

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
    result = build_offer_view(object_model=raw_offer)

    # assert
    assert result.is_manual is is_manual


@pytest.mark.gen_test
@pytest.mark.parametrize('category, currency, expected', [
    (Category.bed_rent, Currency.rur, '123 ₽/мес.'),
    (Category.bed_rent, Currency.usd, '123 $/мес.'),
    (Category.bed_rent, Currency.eur, '123 €/мес.'),
    (Category.building_sale, Currency.rur, '123 ₽'),
    (Category.building_sale, Currency.usd, '123 $'),
    (Category.building_sale, Currency.eur, '123 €'),
    (Category.daily_bed_rent, Currency.rur, '123 ₽/сут.'),
    (Category.daily_bed_rent, Currency.usd, '123 $/сут.'),
    (Category.daily_bed_rent, Currency.eur, '123 €/сут.'),
    (Category.daily_bed_rent, None, None),
])
async def test_build_offer_view__price_info(category, currency, expected):
    # arrange
    raw_offer = ObjectModel(
        bargain_terms=BargainTerms(price=123.0, currency=currency),
        category=category,
        phones=[Phone(country_code='1', number='12312')],
    )

    # act
    result = build_offer_view(object_model=raw_offer)

    # assert
    assert result.price_info.exact == expected


@pytest.mark.gen_test
@pytest.mark.parametrize('category, currency, expected', [
    (Category.office_rent, Currency.rur, [f'от 500', f'до 833 ₽/мес']),
    (Category.office_rent, Currency.usd, [f'от 500', f'до 833 $/мес']),
    (Category.office_rent, Currency.eur, [f'от 500', f'до 833 €/мес']),
    (Category.flat_sale, None, None),
])
async def test_build_offer_view__price_info__can_parts(category, currency, expected):
    # arrange
    raw_offer = ObjectModel(
        bargain_terms=BargainTerms(
            price=100.0,
            price_type=PriceType.square_meter,
            currency=currency
        ),
        category=category,
        phones=[Phone(country_code='1', number='12312')],
        min_area=60.0,
        max_area=100.0,
        can_parts=True
    )

    # act
    result = build_offer_view(object_model=raw_offer)

    # assert
    assert result.price_info.range == expected


@pytest.mark.gen_test
@pytest.mark.parametrize('category, prepared, expected', [
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
    (Category.office_rent, dict(lease_type=LeaseType.sublease), ['Субаренда']),
    (Category.office_rent, dict(lease_type=LeaseType.direct), ['Прямая']),

    (Category.flat_sale, dict(sale_type=SaleType.dupt), ['Переуступка']),
    (Category.new_building_flat_sale, dict(sale_type=SaleType.dupt), ['Переуступка']),
])
async def test_build_offer_view__features(category, prepared, expected):
    # arrange
    raw_offer = ObjectModel(
        bargain_terms=BargainTerms(price=123.0, **prepared),
        category=category,
        phones=[Phone(country_code='1', number='12312')]
    )

    # act
    result = build_offer_view(object_model=raw_offer)

    # assert
    assert result.features == expected


@pytest.mark.gen_test
@pytest.mark.parametrize('category, expected', [
    (Category.office_sale, ['123 ₽ м²']),
    (Category.new_building_flat_sale, ['123 ₽ м²']),
    (Category.office_rent, [f'123 ₽ за м² в год']),
])
async def test_build_offer_view__features__price(category, expected):
    # arrange
    raw_offer = ObjectModel(
        bargain_terms=BargainTerms(
            price=123.0,
            price_type=PriceType.square_meter,
            currency=Currency.rur
        ),
        category=category,
        phones=[Phone(country_code='1', number='12312')],
    )

    # act
    result = build_offer_view(object_model=raw_offer)

    # assert
    assert result.features == expected


@pytest.mark.gen_test
@pytest.mark.parametrize('publish_terms, expected', [
    (PublishTerms(autoprolong=True), ['автопродление']),
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
    result = build_offer_view(object_model=raw_offer)

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
    result = build_offer_view(object_model=raw_offer)

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
    result = build_offer_view(object_model=raw_offer)

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
    result = build_offer_view(object_model=raw_offer)

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
async def test_build_offer_view__geo_underground(geo, expected):
    # arrange
    raw_offer = ObjectModel(
        bargain_terms=BargainTerms(price=123.0),
        category=Category.bed_rent,
        phones=[Phone(country_code='1', number='12312')],
        geo=geo
    )

    # act
    result = build_offer_view(object_model=raw_offer)

    # assert
    assert result.geo.underground == expected


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
    result = build_offer_view(object_model=raw_offer)

    # assert
    assert result.geo.newbuilding == expected


@pytest.mark.gen_test
@pytest.mark.parametrize('geo, expected', [
    (None, None),
    (Geo(address=[]), None),
    (Geo(address=[AddressInfo(id=1, type=RealtyAddressType.location)]), []),
    (
        Geo(address=[
            AddressInfo(id=1, type=RealtyAddressType.location, full_name='Москва'),
            AddressInfo(id=1, type=RealtyAddressType.district, full_name='район Краснопресненский'),
            AddressInfo(id=1, type=RealtyAddressType.street, full_name='улица Пушкина'),
            AddressInfo(id=1, type=RealtyAddressType.house, full_name='13к2'),
        ]),
        [
            Address(name='Москва', search_url='', type=AddressType.location),
            Address(name='район Краснопресненский', search_url='', type=AddressType.district),
            Address(name='улица Пушкина', search_url='', type=AddressType.street),
            Address(name='13к2', search_url='', type=AddressType.house)
        ]
    ),
])
async def test_build_offer_view__geo_address(geo, expected):
    # arrange
    raw_offer = ObjectModel(
        bargain_terms=BargainTerms(price=123.0),
        category=Category.bed_rent,
        phones=[Phone(country_code='1', number='12312')],
        geo=geo
    )

    # act
    result = build_offer_view(object_model=raw_offer)

    # assert
    assert result.geo.address == expected
