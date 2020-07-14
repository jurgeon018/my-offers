from pathlib import Path

from cian_functional_test_utils.pytest_plugin import MockResponse


async def test_v2_get_offers_public__offer_not_found__400(http):
    # act
    response = await http.request(
        'POST',
        '/public/v1/get-offer-duplicates/',
        json={'offerId': 165491301, 'type': 'all'},
        headers={'X-Real-UserId': 1111},
        expected_status=400,
    )

    # assert
    assert response.data['errors'][0]['code'] == 'notFound'


async def test_v2_get_offers_public__bad_offer__200(http, pg):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')

    # act
    response = await http.request(
        'POST',
        '/public/v1/get-offer-duplicates/',
        json={'offerId': 209194477, 'type': 'all'},
        headers={'X-Real-UserId': 29437831},
    )

    # assert
    assert len(response.data['offers']) == 0


async def test_v2_get_offers_public__duplicates_not_found__200(http, pg):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')

    # act
    response = await http.request(
        'POST',
        '/public/v1/get-offer-duplicates/',
        json={'offerId': 231655140, 'type': 'all'},
        headers={'X-Real-UserId': 47135244},
    )

    # assert
    assert len(response.data['offers']) == 0


async def test_v2_get_offers_public__tab_duplicate__duplicates_found__200(http, pg, auction_mock, runtime_settings):
    # arrange
    await runtime_settings.set({'MY_OFFERS.SHOW_SIMILAR_OFFERS.Enabled': False})
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')
    await pg.execute('INSERT INTO offers_duplicates values(231655140, 231655140, \'2020-05-09\')')
    await pg.execute('INSERT INTO offers_duplicates values(231659418, 231655140, \'2020-05-09\')')
    await pg.execute('INSERT INTO offers_duplicates values(173975523, 231655140, \'2020-05-09\')')

    auction_stub = await auction_mock.add_stub(
        method='POST',
        path='/v1/get-bets-by-announcements',
        response=MockResponse(
            body={
                'bets': [{
                    'announcement_id': 173975523,
                    'bet': 12.33,
                }]
            },
        ),
    )

    # act
    response = await http.request(
        'POST',
        '/public/v1/get-offer-duplicates/',
        json={'offerId': 231655140, 'type': 'duplicate'},
        headers={'X-Real-UserId': 47135244},
    )

    # assert
    assert response.data == {
        'offers': [
            {
                'priceInfo': {'exact': '1\xa0200\xa0₽/сут.', 'range': None},
                'geo': {
                    'address': ['Тульская область', 'Тула', 'проспект Ленина', '130'],
                    'underground': None,
                },
                'properties': ['Квартира-студия', '28\xa0м²', '9/14\xa0этаж'],
                'offerId': 173975523,
                'dealType': 'rent',
                'offerType': 'flat',
                'auctionBet': '+\xa012\xa0₽',
                'type': 'duplicate',
                'mainPhotoUrl': 'https://cdn-p.cian.site/images/1/644/244/'
                                'kvartira-tula-prospekt-lenina-442446187-2.jpg',
                'vas': ['auction', 'top3'],
                'displayDate': '2020-05-14T03:06:16.493000+00:00'
            },
            {
                'vas': ['payed'],
                'priceInfo': {'range': None, 'exact': '1\xa0550\xa0000\xa0₽'},
                'properties': ['2-комн.\xa0кв.', '59\xa0м²', '3/3\xa0этаж'],
                'geo': {
                    'underground': None,
                    'address': ['Свердловская область', 'Нижний Тагил', 'улица Циолковского', '37/50']
                },
                'offerId': 231659418,
                'dealType': 'sale',
                'offerType': 'flat',
                'type': 'duplicate',
                'displayDate': '2020-05-09T10:06:29.159746+00:00',
                'mainPhotoUrl': 'https://cdn-p.cian.site/images/6/179/378/'
                                'kvartira-nizhniy-tagil-ulica-ciolkovskogo-873971625-2.jpg',
                'auctionBet': None
            }
        ],
        'page': {'pageCount': 1, 'count': 2, 'canLoadMore': False},
        'tabs': [{'title': 'Все', 'type': 'all', 'count': 2}]
    }

    request = await auction_stub.get_request()
    assert request.data == {'announcementsIds': [173975523]}


async def test_v2_get_offers_public__tab_all__duplicates_found__200(http, pg, auction_mock, runtime_settings):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')
    await pg.execute('INSERT INTO offers_duplicates values(231655140, 231655140, \'2020-05-09\')')
    await pg.execute('INSERT INTO offers_duplicates values(231659418, 231655140, \'2020-05-09\')')
    await pg.execute('INSERT INTO offers_duplicates values(173975523, 231655140, \'2020-05-09\')')

    await runtime_settings.set({'MY_OFFERS.SHOW_SIMILAR_OFFERS.Enabled': False})

    auction_stub = await auction_mock.add_stub(
        method='POST',
        path='/v1/get-bets-by-announcements',
        response=MockResponse(
            body={
                'bets': [{
                    'announcement_id': 173975523,
                    'bet': 12.33,
                }]
            },
        ),
    )

    # act
    response = await http.request(
        'POST',
        '/public/v1/get-offer-duplicates/',
        json={'offerId': 231655140, 'type': 'all'},
        headers={'X-Real-UserId': 47135244},
    )

    # assert
    assert response.data == {
        'offers': [
            {
                'priceInfo': {'exact': '1\xa0200\xa0₽/сут.', 'range': None},
                'geo': {
                    'address': ['Тульская область', 'Тула', 'проспект Ленина', '130'],
                    'underground': None,
                },
                'properties': ['Квартира-студия', '28\xa0м²', '9/14\xa0этаж'],
                'offerId': 173975523,
                'dealType': 'rent',
                'offerType': 'flat',
                'auctionBet': '+\xa012\xa0₽',
                'type': 'duplicate',
                'mainPhotoUrl': 'https://cdn-p.cian.site/images/1/644/244/'
                                'kvartira-tula-prospekt-lenina-442446187-2.jpg',
                'vas': ['auction', 'top3'],
                'displayDate': '2020-05-14T03:06:16.493000+00:00'
            },
            {
                'vas': ['payed'],
                'priceInfo': {'range': None, 'exact': '1\xa0550\xa0000\xa0₽'},
                'properties': ['2-комн.\xa0кв.', '59\xa0м²', '3/3\xa0этаж'],
                'geo': {
                    'underground': None,
                    'address': ['Свердловская область', 'Нижний Тагил', 'улица Циолковского', '37/50']
                },
                'offerId': 231659418,
                'dealType': 'sale',
                'offerType': 'flat',
                'type': 'duplicate',
                'displayDate': '2020-05-09T10:06:29.159746+00:00',
                'mainPhotoUrl': 'https://cdn-p.cian.site/images/6/179/378/'
                                'kvartira-nizhniy-tagil-ulica-ciolkovskogo-873971625-2.jpg',
                'auctionBet': None
            }
        ],
        'page': {'pageCount': 1, 'count': 2, 'canLoadMore': False},
        'tabs': [{'title': 'Все', 'type': 'all', 'count': 2}]
    }

    request = await auction_stub.get_request()
    assert request.data == {'announcementsIds': [173975523]}


async def test_v2_get_offers_public__whithout_type_parameter(http, pg, auction_mock):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')
    await pg.execute('INSERT INTO offers_duplicates values(231655140, 231655140, \'2020-05-09\')')
    await pg.execute('INSERT INTO offers_duplicates values(173975523, 231655140, \'2020-05-09\')')

    # act
    response = await http.request(
        'POST',
        '/public/v1/get-offer-duplicates/',
        json={'offerId': 231655140},
        headers={'X-Real-UserId': 47135244},
    )

    # assert
    assert len(response.data['offers']) == 1


async def test_v2_get_offers_public__same_building_offers_found__200(http, pg, auction_mock, runtime_settings):
    # arrange
    await runtime_settings.set({'MY_OFFERS.SHOW_SIMILAR_OFFERS.Enabled': False})
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers_same_building.sql')
    await pg.execute('INSERT INTO offers_duplicates values(163885962, 163596314, \'2020-05-09\')')
    await pg.execute('INSERT INTO offers_duplicates values(163596314, 163596314, \'2020-05-09\')')
    await pg.execute('INSERT INTO offers_duplicates values(111111111, 163596314, \'2020-05-09\')')

    auction_stub = await auction_mock.add_stub(
        method='POST',
        path='/v1/get-bets-by-announcements',
        response=MockResponse(
            body={
                'bets': [{
                    'announcement_id': 163564158,
                    'bet': 12.33,
                }]
            },
        ),
    )

    # act
    response = await http.request(
        'POST',
        '/public/v1/get-offer-duplicates/',
        json={'offerId': 163885962, 'type': 'sameBuilding'},
        headers={'X-Real-UserId': 12926195},
    )

    # assert
    assert response.data == {
        'offers': [
            {
                'vas': ['auction', 'premium'],
                'priceInfo': {'range': None, 'exact': '140 000 ₽/мес.'},
                'properties': ['2-комн.\xa0кв.', '53\xa0м²', '2/12\xa0этаж'],
                'geo': {
                    'underground': {'name': 'Маяковская', 'lineColor': '00701A', 'regionId': 1},
                    'address': ['Москва', 'Большая Садовая улица', '5к1']
                },
                'offerId': 163564158,
                'dealType': 'rent',
                'offerType': 'flat',
                'type': 'sameBuilding',
                'displayDate': '2017-09-22T23:08:28.277000+00:00',
                'mainPhotoUrl': 'http://master.images.dev3.cian.ru/v1/view/8/503/603/'
                                'kvartira-moskva-bolshaya-sadovaya-ulica-306305809-2.jpg',
                'auctionBet': '+\xa012\xa0₽'
            }
        ],
        'page': {'pageCount': 1, 'count': 1, 'canLoadMore': False},
        'tabs': [{'title': 'Все', 'type': 'all', 'count': 1}]
    }

    request = await auction_stub.get_request()
    assert request.data == {'announcementsIds': [163564158]}


async def test_v2_get_offers_public__same_building_offers_not_found__200(http, pg):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers_same_building.sql')

    # act
    response = await http.request(
        'POST',
        '/public/v1/get-offer-duplicates/',
        json={'offerId': 163569999, 'type': 'sameBuilding'},
        headers={'X-Real-UserId': 8048745},
    )

    # assert
    assert len(response.data['offers']) == 0


async def test_v2_get_offers_public__same_building_offers_not_found__offer_without_house_id__200(http, pg):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers_same_building.sql')

    # act
    response = await http.request(
        'POST',
        '/public/v1/get-offer-duplicates/',
        json={'offerId': 165459837, 'type': 'sameBuilding'},
        headers={'X-Real-UserId': 15059798},
    )

    # assert
    assert len(response.data['offers']) == 0


async def test_v2_get_offers_public__same_building_offers_not_found__offer_without_price__200(http, pg):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers_same_building.sql')

    # act
    response = await http.request(
        'POST',
        '/public/v1/get-offer-duplicates/',
        json={'offerId': 165459855, 'type': 'sameBuilding'},
        headers={'X-Real-UserId': 15059798},
    )

    # assert
    assert len(response.data['offers']) == 0


async def test_v2_get_offers_public__similar_offers_found__200(http, pg, auction_mock, runtime_settings):
    # arrange
    await runtime_settings.set({'MY_OFFERS.SHOW_SIMILAR_OFFERS.Enabled': True})
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers_similar.sql')

    # act
    response = await http.request(
        'POST',
        '/public/v1/get-offer-duplicates/',
        json={'offerId': 162730477, 'type': 'similar'},
        headers={'X-Real-UserId': 8088578},
    )

    # assert
    assert response.data == {
        'offers': [
            {
                'vas': ['premium'],
                'priceInfo': {'range': None, 'exact': '6 837 729 ₽'},
                'properties': ['1-комн. кв.', '37 м²', '9/13 этаж'],
                'geo': {
                    'underground': {'name': 'Кунцевская', 'lineColor': '03238B', 'regionId': 1},
                    'address': ['Москва', 'улица Петра Алексеева', '12АС1']
                },
                'offerId': 162729892,
                'dealType': 'sale',
                'offerType': 'flat',
                'type': 'similar',
                'displayDate': '2019-02-21T10:30:56.847000+00:00',
                'mainPhotoUrl': 'http://master.images.dev3.cian.ru/v1/view/9/403/692/novostroyka-moskva-ulica-petra'
                                '-alekseeva-296304975-2.jpg',
                'auctionBet': None
            }
        ],
        'page': {'pageCount': 1, 'count': 1, 'canLoadMore': False},
        'tabs': [
            {'title': 'Все', 'type': 'all', 'count': 2},
            {'title': 'В этом доме', 'type': 'sameBuilding', 'count': 1},
            {'title': 'Похожие рядом', 'type': 'similar', 'count': 1},
        ]
    }


async def test_v2_get_offers_public__similar_offers_not_found_in_bd__200(http, pg):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers_similar.sql')

    # act
    response = await http.request(
        'POST',
        '/public/v1/get-offer-duplicates/',
        json={'offerId': 165516518, 'type': 'similar'},
        headers={'X-Real-UserId': 15137826},
    )

    # assert
    assert len(response.data['offers']) == 0


async def test_v2_get_offers_public__similar_offers_not_found__offer_without_district_id__200(http, pg):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers_similar.sql')

    # act
    response = await http.request(
        'POST',
        '/public/v1/get-offer-duplicates/',
        json={'offerId': 161950566, 'type': 'similar'},
        headers={'X-Real-UserId': 13328695},
    )

    # assert
    assert len(response.data['offers']) == 0


async def test_v2_get_offers_public__tab_all__offers_found__200(http, pg, auction_mock, runtime_settings):
    # arrange
    await runtime_settings.set({'MY_OFFERS.SHOW_SIMILAR_OFFERS.Enabled': True})
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers_similar_tab_all.sql')
    await pg.execute('INSERT INTO offers_duplicates values(236308049, 236308049, \'2020-05-09\')')
    await pg.execute('INSERT INTO offers_duplicates values(236213060, 236308049, \'2020-05-09\')')
    await pg.execute('INSERT INTO offers_duplicates values(236331615, 236308049, \'2020-05-09\')')
    await pg.execute('INSERT INTO offers_duplicates values(224829657, 236308049, \'2020-05-09\')')
    await pg.execute('INSERT INTO offers_duplicates values(236619358, 236308049, \'2020-05-09\')')
    # act
    response = await http.request(
        'POST',
        '/public/v1/get-offer-duplicates/',
        json={
            'offerId': 236308049,
            'type': 'all',
            'pagination': {
                'limit': 3,
                'page': 2
            }
        },
        headers={'X-Real-UserId': 29641859},
    )

    # assert
    assert response.data == {
        'offers': [
            {
                'vas': ['payed'],
                'priceInfo': {'range': None, 'exact': '55\xa0000\xa0₽/мес.'},
                'properties': ['3-комн.\xa0кв.', '67 м²', '20/25 этаж'],
                'geo': {
                    'underground': None,
                    'address': ['Краснодарский край', 'Сочи', 'Пластунская улица', '123']
                },
                'offerId': 224829657,
                'dealType': 'rent',
                'offerType': 'flat',
                'type': 'duplicate',
                'displayDate': '2020-07-01T22:50:00.793000+00:00',
                'mainPhotoUrl': 'https://cdn-p.cian.site/images/0/364/618/kvartira-sochi-plastunskaya-'
                                'ulica-816463094-2.jpg',
                'auctionBet': None
            },
            {
                'vas': ['payed'],
                'priceInfo': {'range': None, 'exact': '30\xa0000\xa0₽/мес.'},
                'properties': ['1-комн.\xa0кв.', '36 м²', '18/21 этаж'],
                'geo': {
                    'underground': None,
                    'address': ['Краснодарский край', 'Сочи', 'Пластунская улица', '123']
                },
                'offerId': 233353644,
                'dealType': 'rent',
                'offerType': 'flat',
                'type': 'sameBuilding',
                'displayDate': '2020-07-03T07:50:23.673000+00:00',
                'mainPhotoUrl': 'https://cdn-p.cian.site/images/3/086/788/kvartira-sochi-plastunskaya-'
                                'ulica-887680397-2.jpg',
                'auctionBet': None
            },
            {
                'vas': [],
                'priceInfo': {'range': None, 'exact': '25 000 ₽/мес.'},
                'properties': ['1-комн. кв.', '33 м²', '4/7 этаж'],
                'geo': {
                    'underground': None,
                    'address': ['Краснодарский край', 'Сочи', 'Макаренко мкр', 'улица Ботаническая', '34']
                },
                'offerId': 177300443,
                'dealType': 'rent',
                'offerType': 'flat',
                'type': 'similar',
                'displayDate': '2020-07-08T12:28:46.727000+00:00',
                'mainPhotoUrl': 'https://cdn-p.cian.site/images/3/572/154/kvartira-makarenko-'
                                'botanicheskaya-ulica-451275372-2.jpg',
                'auctionBet': None
            }
        ],
        'page': {'pageCount': 2, 'count': 6, 'canLoadMore': False},
        'tabs': [
            {'title': 'Все', 'type': 'all', 'count': 6},
            {'title': 'Дубли', 'type': 'duplicate', 'count': 4},
            {'title': 'В этом доме', 'type': 'sameBuilding', 'count': 1},
            {'title': 'Похожие рядом', 'type': 'similar', 'count': 1},

        ]
    }
