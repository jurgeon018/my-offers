import pytest
from cian_test_utils import future

from my_offers import enums
from my_offers.entities.get_offers import GetOffer, Statistics
from my_offers.entities.offer_view_model import OfferGeo, PriceInfo, Underground
from my_offers.enums.offer_address import AddressType
from my_offers.repositories.monolith_cian_announcementapi.entities import (
    AddressInfo,
    BargainTerms,
    Building,
    Geo,
    Land,
    ObjectModel,
    Phone,
    Photo,
    PublishTerm,
    PublishTerms,
    TariffIdentificator,
    UndergroundInfo,
)
from my_offers.repositories.monolith_cian_announcementapi.entities.bargain_terms import (
    Currency,
    LeaseType,
    PriceType,
    SaleType,
)
from my_offers.repositories.monolith_cian_announcementapi.entities.land import AreaUnitType
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category, FlatType, Source
from my_offers.repositories.monolith_cian_announcementapi.entities.publish_term import Services
from my_offers.repositories.monolith_cian_announcementapi.entities.tariff_identificator import TariffGridType
from my_offers.services.offer_view.offer_view import build_offer_view
from my_offers.services.offers.enrich.enrich_data import EnrichData


@pytest.fixture(name='enrich_data_mock')
def enrich_data_fixture():
    return EnrichData(statistics={}, auctions={}, jk_urls={}, geo_urls={})


def test_build_offer_view(enrich_data_mock):
    # arrange
    raw_offer = ObjectModel(
        id=111,
        bargain_terms=BargainTerms(price=123),
        category=Category.flat_rent,
        phones=[Phone(country_code='1', number='12312')]
    )
    expected_result = GetOffer(
        main_photo_url=None,
        title='',
        url='https://cian.ru/rent/flat/111',
        geo=OfferGeo(address=None, newbuilding=None, underground=None),
        subagent=None,
        price_info=PriceInfo(exact=None, range=None),
        features=[],
        publish_features=[],
        vas=[],
        is_from_package=False,
        is_manual=False,
        is_publication_time_ends=False,
        created_at=None,
        id=111,
        statistics=Statistics(),
        auction=None,
    )

    # act
    result = build_offer_view(object_model=raw_offer, enrich_data=enrich_data_mock)

    # assert
    assert result == expected_result


@pytest.mark.parametrize('category, prepared, building, expected', (
    (
        Category.office_sale,
        dict(total_area=60.0, floor_number=3), Building(floors_count=19),
        'Офис, 60 м², 3/19 этаж'
    ),
    (
        Category.office_sale,
        dict(total_area=60.0, floor_number=3), None,
        'Офис, 60 м², 3 этаж'
    ),
    (
        Category.office_sale,
        dict(total_area=60.0, floor_number=-1), None,
        'Офис, 60 м², полуподвал'
    ),
    (
        Category.office_sale,
        dict(total_area=60.0, floor_number=-2), None,
        'Офис, 60 м², подвал'
    ),
    (
        Category.office_sale,
        dict(total_area=60.0, min_area=10.0, can_parts=True), None,
        'Офис, от 10 до 60 м²'
    ),
    (
        Category.office_sale,
        dict(total_area=60.0), None,
        'Офис, 60 м²'
    ),
    (Category.shopping_area_sale, dict(total_area=60.0), None, 'Торговая площадь, 60 м²'),
    (Category.shopping_area_rent, dict(total_area=60.0), None, 'Торговая площадь, 60 м²'),
    (Category.warehouse_sale, dict(total_area=60.0), None, 'Склад, 60 м²'),
    (Category.warehouse_rent, dict(total_area=60.0), None, 'Склад, 60 м²'),
    (Category.free_appointment_object_sale, dict(total_area=60.0), None, 'Помещение свободного назначения, 60 м²'),
    (Category.free_appointment_object_sale, dict(total_area=60.0), None, 'Помещение свободного назначения, 60 м²'),
    (Category.public_catering_rent, dict(total_area=60.0), None, 'Общепит, 60 м²'),
    (Category.public_catering_sale, dict(total_area=60.0), None, 'Общепит, 60 м²'),
    (Category.garage_sale, dict(total_area=60.0), None, 'Гараж, 60 м²'),
    (Category.garage_rent, dict(total_area=60.0), None, 'Гараж, 60 м²'),
    (Category.industry_sale, dict(total_area=60.0), None, 'Производство, 60 м²'),
    (Category.industry_rent, dict(total_area=60.0), None, 'Производство, 60 м²'),
    (Category.car_service_sale, dict(total_area=60.0), None, 'Автосервис, 60 м²'),
    (Category.car_service_rent, dict(total_area=60.0), None, 'Автосервис, 60 м²'),
    (Category.business_rent, dict(total_area=60.0), None, 'Готовый бизнес, 60 м²'),
    (Category.business_sale, dict(total_area=60.0), None, 'Готовый бизнес, 60 м²'),
    (Category.building_sale, dict(total_area=60.0), None, 'Здание, 60 м²'),
    (Category.building_rent, dict(total_area=60.0), None, 'Здание, 60 м²'),
    (Category.domestic_services_rent, dict(total_area=60.0), None, 'Бытовые услуги, 60 м²'),
    (Category.domestic_services_rent, dict(total_area=60.0), None, 'Бытовые услуги, 60 м²'),
))
def test_build_offer_view__tittle_commercial(category, prepared, building, expected, enrich_data_mock):
    # arrange
    raw_offer = ObjectModel(
        bargain_terms=BargainTerms(price=123),
        category=category,
        phones=[Phone(country_code='1', number='12312')],
        building=building,
        **prepared
    )

    # act
    result = build_offer_view(object_model=raw_offer, enrich_data=enrich_data_mock)

    # assert
    assert result.title == expected


@pytest.mark.parametrize('category, prepared, building, expected', [
    (Category.house_sale, dict(total_area=60.0), None, 'Дом, 60 м²'),
    (Category.house_rent, dict(total_area=60.0), None, 'Дом, 60 м²'),
    (Category.daily_house_rent, dict(total_area=60.0), None, 'Дом, 60 м²'),
    (Category.house_share_sale, dict(total_area=60.0), None, 'Часть дома, 60 м²'),
    (Category.house_share_rent, dict(total_area=60.0), None, 'Часть дома, 60 м²'),
    (Category.cottage_rent, dict(total_area=60.0), None, 'Коттедж, 60 м²'),
    (Category.cottage_sale, dict(total_area=60.0), None, 'Коттедж, 60 м²'),
    (Category.townhouse_rent, dict(total_area=60.0), None, 'Таунхаус, 60 м²'),
    (Category.townhouse_sale, dict(total_area=60.0), None, 'Таунхаус, 60 м²'),
])
def test_build_offer_view__tittle_suburban(category, prepared, building, expected, enrich_data_mock):
    # arrange
    raw_offer = ObjectModel(
        bargain_terms=BargainTerms(price=123),
        category=category,
        phones=[Phone(country_code='1', number='12312')],
        building=building,
        **prepared
    )

    # act
    result = build_offer_view(object_model=raw_offer, enrich_data=enrich_data_mock)

    # assert
    assert result.title == expected


@pytest.mark.parametrize('category, prepared, building, expected', [
    (
        Category.daily_flat_rent,
        dict(rooms_count=1, total_area=60.0, floor_number=3), Building(floors_count=19),
        '1-комн. кв., 60 м², 3/19 этаж'
    ),
    (
        Category.flat_sale,
        dict(rooms_count=1, total_area=60.0, floor_number=3), None,
        '1-комн. кв., 60 м², 3 этаж'
    ),
    (
        Category.flat_rent,
        dict(rooms_count=1, total_area=60.0, floor_number=3, is_apartments=True), Building(floors_count=19),
        '1-комн. кв., 60 м², 3/19 этаж'
    ),
    (
        Category.flat_rent,
        dict(rooms_count=5, total_area=60.0, floor_number=3, is_apartments=True), Building(floors_count=19),
        '5-комн. кв., 60 м², 3/19 этаж'
    ),
    (
        Category.flat_rent,
        dict(rooms_count=8, total_area=60.0, floor_number=3), Building(floors_count=19),
        'Многокомн. кв., 60 м², 3/19 этаж'
    ),
    (
        Category.room_rent,
        dict(total_area=60.0, floor_number=3), Building(floors_count=19),
        f'Комната, 60 м², 3/19 этаж'),
    (
        Category.daily_room_rent,
        dict(total_area=60.0, floor_number=3), Building(floors_count=19),
        f'Комната, 60 м², 3/19 этаж'
    ),
    (
        Category.bed_rent,
        dict(total_area=60.0, floor_number=3), Building(floors_count=19),
        f'Койко-место, 60 м², 3/19 этаж'
    ),
    (
        Category.daily_bed_rent,
        dict(total_area=60.0, floor_number=3), Building(floors_count=19),
        f'Койко-место, 60 м², 3/19 этаж'
    ),
    (
        Category.flat_share_sale,
        dict(total_area=60.0, floor_number=3), Building(floors_count=19),
        f'Доля в квартире, 60 м², 3/19 этаж'
    ),
    (
        Category.flat_rent,
        dict(total_area=60.0, floor_number=3, flat_type=FlatType.studio), Building(floors_count=19),
        f'Квартира-студия, 60 м², 3/19 этаж'
    ),
    (
        Category.flat_rent,
        dict(total_area=60.0, floor_number=3, flat_type=FlatType.open_plan), Building(floors_count=19),
        f'Квартира со свободной планир., 60 м², 3/19 этаж'
    ),
])
def test_build_offer_view__tittle_flat(category, prepared, building, expected, enrich_data_mock):
    # arrange
    raw_offer = ObjectModel(
        bargain_terms=BargainTerms(price=123),
        category=category,
        phones=[Phone(country_code='1', number='12312')],
        building=building,
        **prepared
    )

    # act
    result = build_offer_view(object_model=raw_offer, enrich_data=enrich_data_mock)

    # assert
    assert result.title == expected


@pytest.mark.parametrize('category, land, expected', [
    (
        Category.land_sale,
        Land(area=16.57, area_unit_type=AreaUnitType.sotka),
        'Земельный участок, 16.57 сот.'
    ),
    (
        Category.land_sale,
        Land(area=16.57, area_unit_type=AreaUnitType.hectare),
        'Земельный участок, 16.57 га.'
    ),
    (
        Category.commercial_land_rent,
        Land(area=16.57, area_unit_type=AreaUnitType.hectare),
        'Коммерческая земля, 16.57 га.'
    ),
    (
        Category.commercial_land_rent,
        Land(area=16.57, area_unit_type=AreaUnitType.sotka),
        'Коммерческая земля, 16.57 сот.'
    ),

])
def test_build_offer_view__tittle__land(category, land, expected, enrich_data_mock):
    # arrange
    raw_offer = ObjectModel(
        bargain_terms=BargainTerms(price=123),
        category=category,
        phones=[Phone(country_code='1', number='12312')],
        land=land
    )

    # act
    result = build_offer_view(object_model=raw_offer, enrich_data=enrich_data_mock)

    # assert
    assert result.title == expected


@pytest.mark.parametrize('photos, expected', [
    ([Photo(mini_url='http://photo_url.ru/1_mini.jpg')], 'http://photo_url.ru/1_mini.jpg'),
    ([Photo(mini_url=None)], None),
    ([], None),
    (None, None),
])
def test_build_offer_view__main_photo_url(photos, expected, enrich_data_mock):
    # arrange
    raw_offer = ObjectModel(
        bargain_terms=BargainTerms(price=123),
        category=Category.building_rent,
        phones=[Phone(country_code='1', number='12312')],
        photos=photos
    )

    # act
    result = build_offer_view(object_model=raw_offer, enrich_data=enrich_data_mock)

    # assert
    assert result.main_photo_url == expected


@pytest.mark.parametrize('category, expected', [
    (Category.room_rent, 'https://cian.ru/rent/flat/123'),
    (Category.office_rent, 'https://cian.ru/rent/commercial/123'),
    (Category.house_rent, 'https://cian.ru/rent/suburban/123'),
    (Category.new_building_flat_sale, 'https://cian.ru/sale/flat/123'),
])
def test_build_offer_view__offer_url(category, expected, enrich_data_mock):
    # arrange
    raw_offer = ObjectModel(
        id=123,
        bargain_terms=BargainTerms(price=123),
        category=category,
        phones=[Phone(country_code='1', number='12312')],
    )

    # act
    result = build_offer_view(object_model=raw_offer, enrich_data=enrich_data_mock)

    # assert
    assert result.url == expected


def test_build_offer_view__subagent(enrich_data_mock):
    # arrange
    raw_offer = ObjectModel(
        bargain_terms=BargainTerms(price=123),
        category=Category.building_rent,
        phones=[Phone(country_code='1', number='12312')]
    )

    # act
    result = build_offer_view(object_model=raw_offer, enrich_data=enrich_data_mock)

    # assert
    assert result.subagent is None


@pytest.mark.parametrize('source, is_manual', [
    (Source.upload, True),
    (Source.website, False),
    (Source.mobile_app, False),
])
def test_build_offer_view__is__from_import(source, is_manual, enrich_data_mock):
    # arrange
    raw_offer = ObjectModel(
        source=source,
        bargain_terms=BargainTerms(price=123),
        category=Category.building_rent,
        phones=[Phone(country_code='1', number='12312')]
    )

    # act
    result = build_offer_view(object_model=raw_offer, enrich_data=enrich_data_mock)

    # assert
    assert result.is_manual is is_manual


@pytest.mark.parametrize('category, currency, price_type, expected', [
    (Category.office_rent, Currency.rur, PriceType.square_meter, '100 000 ₽/мес.'),
    (Category.bed_rent, Currency.usd, None, '10 000 $/мес.'),
    (Category.bed_rent, Currency.eur, None, '10 000 €/мес.'),
    (Category.building_sale, Currency.rur, None, '10 000 ₽'),
    (Category.building_sale, Currency.usd, None, '10 000 $'),
    (Category.building_sale, Currency.eur, None, '10 000 €'),
    (Category.daily_bed_rent, Currency.rur, None, '10 000 ₽/сут.'),
    (Category.daily_bed_rent, Currency.usd, None, '10 000 $/сут.'),
    (Category.daily_bed_rent, Currency.eur, None, '10 000 €/сут.'),
    (Category.daily_bed_rent, None, None, None),
])
def test_build_offer_view__price_info(category, currency, price_type, expected, enrich_data_mock):
    # arrange
    raw_offer = ObjectModel(
        bargain_terms=BargainTerms(price=10000.0, currency=currency, price_type=price_type),
        category=category,
        total_area=10.0,
        phones=[Phone(country_code='1', number='12312')],
    )

    # act
    result = build_offer_view(object_model=raw_offer, enrich_data=enrich_data_mock)

    # assert
    assert result.price_info.exact == expected


@pytest.mark.parametrize('category, currency, expected', [
    (Category.office_rent, Currency.rur, [f'от 50 000', f'до 83 333 ₽/мес']),
    (Category.office_rent, Currency.usd, [f'от 50 000', f'до 83 333 $/мес']),
    (Category.office_rent, Currency.eur, [f'от 50 000', f'до 83 333 €/мес']),
    (Category.flat_sale, None, None),
])
def test_build_offer_view__price_info__can_parts(category, currency, expected, enrich_data_mock):
    # arrange
    raw_offer = ObjectModel(
        bargain_terms=BargainTerms(
            price=10000.0,
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
    result = build_offer_view(object_model=raw_offer, enrich_data=enrich_data_mock)

    # assert
    assert result.price_info.range == expected


@pytest.mark.parametrize('category, prepared, expected', [
    (Category.flat_sale, dict(mortgage_allowed=True), ['Возможна ипотека']),
    (Category.flat_sale, dict(sale_type=SaleType.alternative), ['Альтернативная продажа']),
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
    (Category.office_rent, dict(lease_type=LeaseType.direct), ['Прямая аренда']),

    (Category.flat_sale, dict(sale_type=SaleType.dupt), ['Переуступка']),
    (Category.new_building_flat_sale, dict(sale_type=SaleType.dupt), ['Переуступка']),
])
def test_build_offer_view__features(category, prepared, expected, enrich_data_mock):
    # arrange
    raw_offer = ObjectModel(
        bargain_terms=BargainTerms(price=123.0, **prepared, currency=Currency.rur),
        category=category,
        phones=[Phone(country_code='1', number='12312')],
    )

    # act
    result = build_offer_view(object_model=raw_offer, enrich_data=enrich_data_mock)

    # assert
    assert result.features == expected


@pytest.mark.parametrize('category, price_type, expected', [
    (Category.office_sale, PriceType.square_meter, ['123 000 ₽ м²']),
    (Category.new_building_flat_sale, PriceType.square_meter, ['123 000 ₽ м²']),
    (Category.office_rent, PriceType.square_meter, [f'1 476 000 ₽ за м² в год']),
    (Category.office_sale, PriceType.all, [f'12 300 ₽ за м²']),
])
def test_build_offer_view__features__price(category, price_type, expected, enrich_data_mock):
    # arrange
    raw_offer = ObjectModel(
        bargain_terms=BargainTerms(
            price=123000.0,
            price_type=price_type,
            currency=Currency.rur,
        ),
        category=category,
        total_area=10.0,
        phones=[Phone(country_code='1', number='12312')],
    )

    # act
    result = build_offer_view(object_model=raw_offer, enrich_data=enrich_data_mock)

    # assert
    assert result.features == expected


@pytest.mark.parametrize('publish_terms, expected', [
    (PublishTerms(autoprolong=True), ['автопродление']),
])
def test_build_offer_view__publish_features(publish_terms, expected, enrich_data_mock):
    # arrange
    raw_offer = ObjectModel(
        bargain_terms=BargainTerms(price=123.0),
        publish_terms=publish_terms,
        category=Category.bed_rent,
        phones=[Phone(country_code='1', number='12312')]
    )

    # act
    result = build_offer_view(object_model=raw_offer, enrich_data=enrich_data_mock)

    # assert
    assert result.publish_features == expected


@pytest.mark.parametrize('terms, expected', [
    (
        [PublishTerm(services=[Services.calltracking, Services.paid])],
        [enums.OfferVas.payed]
    ),
    (
        [PublishTerm(services=[Services.calltracking, Services.paid]), PublishTerm(services=[Services.top3])],
        [enums.OfferVas.payed, enums.OfferVas.top3]
    ),
])
def test_build_offer_view__vas(terms, expected, enrich_data_mock):
    # arrange
    raw_offer = ObjectModel(
        bargain_terms=BargainTerms(price=123.0),
        publish_terms=PublishTerms(terms=terms),
        category=Category.bed_rent,
        phones=[Phone(country_code='1', number='12312')]
    )

    # act
    result = build_offer_view(object_model=raw_offer, enrich_data=enrich_data_mock)

    # assert
    assert result.vas == expected


@pytest.mark.parametrize('publish_terms, expected', [
    (None, False),
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
            tariff_grid_type=TariffGridType.service_package_group))]),
        True
    )
])
def test_build_offer_view__is_from_package(publish_terms, expected, enrich_data_mock):
    # arrange
    raw_offer = ObjectModel(
        bargain_terms=BargainTerms(price=123.0),
        publish_terms=publish_terms,
        category=Category.bed_rent,
        phones=[Phone(country_code='1', number='12312')]
    )

    # act
    result = build_offer_view(object_model=raw_offer, enrich_data=enrich_data_mock)

    # assert
    assert result.is_from_package is expected


def test_build_offer_view__is_publication_time_ends(enrich_data_mock):
    # arrange
    raw_offer = ObjectModel(
        bargain_terms=BargainTerms(price=123.0),
        category=Category.bed_rent,
        phones=[Phone(country_code='1', number='12312')]
    )

    # act
    result = build_offer_view(object_model=raw_offer, enrich_data=enrich_data_mock)

    # assert
    assert result.is_publication_time_ends is False


@pytest.mark.parametrize('geo, expected', [
    (None, None),
    (Geo(undergrounds=[], address=[]), None),
    (
        Geo(
            undergrounds=[UndergroundInfo(line_color='12321', name='Сокольники', is_default=True)],
            address=[AddressInfo(id=1, type=AddressType.location)]
        ),
        Underground(search_url='', region_id=1, line_color='#12321', name='Сокольники')
    )
])
def test_build_offer_view__geo_underground(mocker, geo, expected, enrich_data_mock):
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
    build_offer_view(object_model=raw_offer, enrich_data=enrich_data_mock)

    # assert
    prepare_geo_mock.assert_called_once()
