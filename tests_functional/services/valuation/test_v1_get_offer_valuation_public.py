from pathlib import Path

from cian_functional_test_utils.pytest_plugin import MockResponse


async def test_v1_get_offer_valuation__200(http_client, pg, price_estimator_mock):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers_for_valuation.sql')

    price_estimator_stub = await price_estimator_mock.add_stub(
        method='POST',
        path='/v1/get-estimation-for-realtors/',
        response=MockResponse(
            body={
                'liquidityPeriods': {
                    'periodWithPromotion': {
                        'maxSellingTerm': 90,
                        'minSellingTerm': 75,
                    },
                    'regularPeriod': {
                        'maxSellingTerm': None,
                        'minSellingTerm': 120,
                    },
                },
                'prices': {
                    'price': 58_160_000,
                    'priceMax': 63_970_000,
                    'priceMin': 52_340_000,
                },
                'url': 'http://www.master.dev3.cian.ru/kalkulator-nedvizhimosti/?address=%D0%9C%D0%BE%D1%81%D0%BA%D0%B'
                       '2%D0%B0%2C+%D0%9D%D0%B8%D0%BA%D0%B8%D1%82%D1%81%D0%BA%D0%B8%D0%B9+%D0%B1%D1%83%D0%BB%D1%8C%D0%'
                       'B2%D0%B0%D1%80%2C+12&totalArea=115&roomsCount=4&offerId=153126220'
            },
        ),
    )

    # act

    response = await http_client.request(
        'POST',
        '/public/v1/get-offer-valuation/',
        json={'offerId': 153126220},
        headers={'X-Real-UserId': 2994068},
    )

    # assert
    request = await price_estimator_stub.get_request()
    assert request.data == {
        'address': 'Москва, Никитский бульвар, 12',
        'area': 115.0,
        'dealType': 'sale',
        'houseId': 1691187,
        'offerId': 153126220,
        'price': 54_000_000,
        'roomsCount': 4,
        'filters': [
            {
                'key': 'floor',
                'value': ['floorOne']
            },
            {
                'key': 'repairType',
                'value': ['repairTypeEuro']
            }
        ],
    }
    assert response.data == {
        'valuationOptions': [
            {
                'description': 'Рыночная\xa0цена\xa0этой\xa0квартиры',
                'value': '58,16 млн\xa0₽'
            },
            {
                'description': 'Диапазон\xa0цены',
                'value': '52,34—63,97\xa0млн\xa0₽'
            },
            {
                'description': 'Прогнозируемый срок продажи при текущей цене квартиры и продвижении',
                'value': '120+\xa0дней'
            }
        ],
        'infoRelativeMarket': {
            'hint': 'По данным Циан.Аналитика за предыдущий год',
            'text': 'Квартиры с рыночной ценой и продвижением в среднем продаются в течение 45 дней',
            'title': 'Ваша цена рыночная',
            'priceEstimate': 'inMarket'
        },
        'valuationBlockLinkShare': 'http://www.master.dev3.cian.ru/kalkulator-nedvizhimosti/?address=%D0%9C%D0%BE%D1%81'
                                   '%D0%BA%D0%B2%D0%B0%2C+%D0%9D%D0%B8%D0%BA%D0%B8%D1%82%D1%81%D0%BA%D0%B8%D0%B9+%D0%B1'
                                   '%D1%83%D0%BB%D1%8C%D0%B2%D0%B0%D1%80%2C+12&totalArea=115&roomsCount=4&offerId=15312'
                                   '6220',
        'valuationBlockLinkReport': 'http://www.master.dev3.cian.ru/kalkulator-nedvizhimosti/?address=%D0%9C%D0%BE%D1%8'
                                    '1%D0%BA%D0%B2%D0%B0%2C+%D0%9D%D0%B8%D0%BA%D0%B8%D1%82%D1%81%D0%BA%D0%B8%D0%B9+%D0%'
                                    'B1%D1%83%D0%BB%D1%8C%D0%B2%D0%B0%D1%80%2C+12&totalArea=115&roomsCount=4&offerId=15'
                                    '3126220'
    }


async def test_v1_get_offer_valuation__price_estimator_None_response__error(http_client, pg, price_estimator_mock):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers_for_valuation.sql')

    await price_estimator_mock.add_stub(
        method='POST',
        path='/v1/get-estimation-for-realtors/',
        response=MockResponse(
            body={
                'liquidity_periods': None,
                'prices': None,
                'url': None,
            }
        ),
    )

    # act
    response = await http_client.request(
        'POST',
        '/public/v1/get-offer-valuation/',
        json={'offerId': 153126220},
        headers={'X-Real-UserId': 2994068},
        expected_status=400,
    )

    # assert
    assert response.data == {
        'errors': [
            {
                'key': 'noValuation',
                'code': 'didNotGetValuation',
                'message': 'did not get valuation for offer from mcs price-estimator'
            }
        ],
        'message': 'did not get valuation for offer from mcs price-estimator'
    }


async def test_v1_get_offer_valuation__price_estimator_500__error(http_client, pg, price_estimator_mock):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers_for_valuation.sql')

    await price_estimator_mock.add_stub(
        method='POST',
        path='/v1/get-estimation-for-realtors/',
        response=MockResponse(
            status=500
        ),
    )

    # act
    response = await http_client.request(
        'POST',
        '/public/v1/get-offer-valuation/',
        json={'offerId': 153126220},
        headers={'X-Real-UserId': 2994068},
        expected_status=400,
    )

    # assert
    assert response.data == {
        'errors': [
            {
                'key': 'noValuation',
                'code': 'didNotGetValuation',
                'message': 'did not get valuation for offer from mcs price-estimator'
            }
        ],
        'message': 'did not get valuation for offer from mcs price-estimator'
    }


async def test_v1_get_offer_valuation__error_wrong_offer_category(http_client, pg, price_estimator_mock):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers_for_valuation.sql')

    # act
    response = await http_client.request(
        'POST',
        '/public/v1/get-offer-valuation/',
        json={'offerId': 165197457},
        headers={'X-Real-UserId': 13898800},
        expected_status=400,
    )

    # assert
    assert response.data == {
        'errors': [
            {
                'key': 'offerCategory',
                'code': 'categoryNotSupported',
                'message': 'offer category Category.building_rent is not supported'
            }
        ],
        'message': 'offer category Category.building_rent is not supported'
    }


async def test_v1_get_offer_valuation__no_geo_in_object_model__error(http_client, pg, price_estimator_mock):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers_for_valuation.sql')

    # act
    response = await http_client.request(
        'POST',
        '/public/v1/get-offer-valuation/',
        json={'offerId': 161953060},
        headers={'X-Real-UserId': 12678364},
        expected_status=400,
    )

    # assert
    assert response.data == {
        'errors': [
            {
                'key': 'geo',
                'code': 'valuationNotPoossible',
                'message': 'broken offer object_model, has not right geo address'
            }
        ],
        'message': 'broken offer object_model, has not right geo address'
    }
