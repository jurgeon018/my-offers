import pytest
from cian_test_utils import v
from simple_settings.utils import settings_stub

from my_offers import enums
from my_offers.entities import PriceInfo
from my_offers.helpers.price import get_price_info
from my_offers.helpers.price._price_info import _calc_utilities_delta, _get_price_info
from my_offers.repositories.monolith_cian_announcementapi.entities import (
    BargainTerms,
    Geo,
    LocationPath,
    RentByParts,
    UtilitiesTerms,
)
from my_offers.repositories.monolith_cian_announcementapi.entities.bargain_terms import (
    Currency,
    LeaseTermType,
    LeaseType,
    PaymentPeriod,
    PriceType,
    VatType,
)
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import (
    Category,
    CoworkingOfferType,
    ObjectModel,
)


@pytest.mark.parametrize(
    (
        'bargain_terms',
        'category',
        'can_parts',
        'min_area',
        'max_area',
        'total_area',
        'offer_type',
        'deal_type',
        'expected',
    ),
    (
        (
            BargainTerms(price=10000.0, currency=Currency.rur, price_type=PriceType.all),
            Category.office_sale,
            True,
            10,
            100,
            100,
            enums.OfferType.commercial,
            enums.DealType.sale,
            PriceInfo(exact=None, range=['от\xa01\xa0000', 'до\xa010\xa0000\xa0₽']),
        ),
        (
            BargainTerms(price=10000.0, currency=Currency.rur, price_type=PriceType.all),
            Category.daily_flat_rent,
            True,
            10,
            100,
            100,
            enums.OfferType.flat,
            enums.DealType.rent,
            PriceInfo(exact='10\xa0000\xa0₽/сут.', range=None),
        ),
        (
            BargainTerms(
                price=10000.0,
                currency=Currency.rur,
                price_type=PriceType.square_meter,
                payment_period=PaymentPeriod.annual
            ),
            Category.office_sale,
            True,
            10,
            100,
            100,
            enums.OfferType.commercial,
            enums.DealType.rent,
            PriceInfo(exact=None, range=['от\xa08\xa0334', 'до\xa083\xa0334\xa0₽/мес']),
        ),
        (
            BargainTerms(
                price=10000.0,
                currency=Currency.rur,
                price_type=PriceType.square_meter,
                payment_period=PaymentPeriod.monthly
            ),
            Category.office_sale,
            True,
            10,
            100,
            100,
            enums.OfferType.commercial,
            enums.DealType.rent,
            PriceInfo(exact=None, range=['от\xa0100\xa0000', 'до\xa01\xa0000\xa0000\xa0₽/мес']),
        ),
        (
            BargainTerms(
                price=None,
                currency=Currency.rur,
                price_type=PriceType.square_meter,
                payment_period=PaymentPeriod.monthly
            ),
            Category.office_sale,
            True,
            10,
            100,
            100,
            enums.OfferType.commercial,
            enums.DealType.rent,
            PriceInfo(exact=None, range=None),
        ),
        (
            BargainTerms(
                price=18000.0,
                vat_type=VatType.included,
                currency=Currency.rur,
                price_type=PriceType.square_meter,
                payment_period=PaymentPeriod.annual,
                vat_price=3000.0,
                client_fee=0,
                lease_type=LeaseType.direct,
                vat_included=True,
                prepay_months=1,
                lease_term_type=LeaseTermType.long_term,
            ),
            Category.office_rent,
            False,
            10,
            100,
            100,
            enums.OfferType.commercial,
            enums.DealType.rent,
            PriceInfo(exact='150\xa0000\xa0₽/мес.', range=None),
        ),
    ),

)
def test_get_price_info(
        bargain_terms,
        category,
        can_parts,
        min_area,
        max_area,
        total_area,
        offer_type,
        deal_type,
        expected,
):
    # arrange & act
    result = _get_price_info(
        locations=[1],
        bargain_terms=bargain_terms,
        category=category,
        can_parts=can_parts,
        min_area=min_area,
        max_area=max_area,
        total_area=total_area,
        offer_type=offer_type,
        deal_type=deal_type,
    )

    # assert
    assert result == expected


def test_get_price_info__coworking_office__price_for_all():
    """Цена указана за весь офис, ожидаем цену за рабочее место"""
    # arrange
    bargain_terms = v(BargainTerms(price=10000.0, currency=Currency.rur, price_type=PriceType.all))

    # act
    result = get_price_info(ObjectModel(
        geo=Geo(location_path=LocationPath(child_to_parent=[1])),
        bargain_terms=bargain_terms,
        category=Category.office_rent,
        can_parts=False,
        min_area=None,
        max_area=20,
        total_area=20,
        coworking_offer_type=CoworkingOfferType.office,
        workplace_count=10,
        phones=[],
    ))

    # assert
    assert result == v(PriceInfo(exact='1\xa0000\xa0₽/мес. за рабочее место', range=None))


def test_get_price_info__coworking_office__price_for_workplace():
    """Есть цена за рабочее место"""
    # arrange
    bargain_terms = v(BargainTerms(
        price=10000.0,
        currency=Currency.rur,
        price_type=PriceType.all,
        price_for_workplace=2000,
    ))

    # act
    result = get_price_info(ObjectModel(
        geo=Geo(location_path=LocationPath(child_to_parent=[1])),
        bargain_terms=bargain_terms,
        category=Category.office_rent,
        can_parts=False,
        min_area=None,
        max_area=20,
        total_area=20,
        coworking_offer_type=CoworkingOfferType.office,
        workplace_count=10,
        phones=[],
    ))

    # assert
    assert result == v(PriceInfo(exact='2\xa0000\xa0₽/мес. за рабочее место', range=None))


def test_get_price_info__area_part__price_range():
    """Есть диапазон цены"""
    # arrange
    bargain_terms = v(BargainTerms(
        price=3600.0,
        currency=Currency.rur,
        price_type=PriceType.square_meter,
        payment_period=PaymentPeriod.monthly,
    ))

    # act
    result = get_price_info(ObjectModel(
        geo=Geo(location_path=LocationPath(child_to_parent=[1])),
        bargain_terms=bargain_terms,
        category=Category.office_rent,
        can_parts=True,
        total_area=33,
        phones=[],
        area_parts=[
            RentByParts(area=23, price=3300),
            RentByParts(area=10, price=2000),
        ]
    ))

    # assert
    assert result == PriceInfo(exact=None, range=['от\xa020\xa0000', 'до\xa0118\xa0800\xa0₽/мес'])


@pytest.mark.parametrize(
    ('locations', 'price', 'included_in_price', 'use_include_utilities_terms_regions', 'expected'),
    (
        ([1, 4593], False, None, True, 0),
        ([5], 3000, False, True, 0),
        ([2], 3000, False, False, 0),
        ([1], 3000, False, True, 3000),
        ([5], 3000, False, False, 3000),
        ([5], 3000, True, False, 0),
    )
)
def test__calc_utilities_delta(locations, price, included_in_price, use_include_utilities_terms_regions, expected):
    # arrange
    utilities_terms = UtilitiesTerms(
        included_in_price=included_in_price,
        price=price,
    )

    # act
    with settings_stub(USE_INCLUDE_UTILITIES_TERMS_REGIONS=use_include_utilities_terms_regions,):
        result = _calc_utilities_delta(
            locations=locations,
            utilities_terms=utilities_terms,
        )

    # assert
    assert result == expected
