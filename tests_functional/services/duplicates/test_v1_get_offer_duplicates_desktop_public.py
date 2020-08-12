from pathlib import Path

from cian_functional_test_utils.pytest_plugin import MockResponse


async def test_v1_get_offer_duplicates_desktop_public__offer_not_found__400(http):
    # act
    response = await http.request(
        'POST',
        '/public/v1/get-offers-duplicates-for-desktop/',
        json={'offerId': 165491301, 'type': 'all'},
        headers={'X-Real-UserId': 1111},
        expected_status=400,
    )

    # assert
    assert response.data['errors'][0]['code'] == 'notFound'


async def test_v1_get_offer_duplicates_desktop_public__bad_offer__200(http, pg):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')

    # act
    response = await http.request(
        'POST',
        '/public/v1/get-offers-duplicates-for-desktop/',
        json={'offerId': 209194477, 'type': 'all'},
        headers={'X-Real-UserId': 29437831},
    )

    # assert
    assert len(response.data['offers']) == 0


async def test_v1_get_offer_duplicates_desktop_public__tab_all__duplicates_found__200(http, pg, auction_mock):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')

    await pg.execute(
        'INSERT INTO offers_similars_flat(offer_id, deal_type, sort_date, group_id) '
        'VALUES(231655140, \'sale\', \'2020-08-10\', 231655140)'
    )
    await pg.execute(
        'INSERT INTO offers_similars_flat(offer_id, deal_type, sort_date, group_id) '
        'VALUES(231659418, \'sale\', \'2020-08-10\', 231655140)'
    )
    await pg.execute(
        'INSERT INTO offers_similars_flat(offer_id, deal_type, sort_date, group_id) '
        'VALUES(173975523, \'sale\', \'2020-08-10\', 231655140)'
    )

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
        '/public/v1/get-offers-duplicates-for-desktop/',
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
                'offerId': 173975523,
                'auctionBet': '+\xa012\xa0₽',
                'title': 'Квартира-студия, 28\xa0м², 9/14\xa0этаж',
                'type': 'duplicate',
                'url': 'http://master.dev3.cian.ru/rent/flat/173975523',
                'mainPhotoUrl': 'https://cdn-p.cian.site/images/1/644/244/'
                                'kvartira-tula-prospekt-lenina-442446187-2.jpg',
                'vas': ['auction', 'top3'],
                'displayDate': '2020-05-14T03:06:16.493000+00:00'
            },
            {
                'vas': ['payed'],
                'priceInfo': {'range': None, 'exact': '1\xa0550\xa0000\xa0₽'},
                'geo': {
                    'underground': None,
                    'address': ['Свердловская область', 'Нижний Тагил', 'улица Циолковского', '37/50']
                },
                'offerId': 231659418,
                'title': '2-комн.\xa0кв., 59\xa0м², 3/3\xa0этаж',
                'type': 'duplicate',
                'url': 'http://master.dev3.cian.ru/sale/flat/231659418',
                'displayDate': '2020-05-09T10:06:29.159746+00:00',
                'mainPhotoUrl': 'https://cdn-p.cian.site/images/6/179/378/'
                                'kvartira-nizhniy-tagil-ulica-ciolkovskogo-873971625-2.jpg',
                'auctionBet': None
            }
        ],
        'page': {'pageCount': 1, 'count': 2, 'canLoadMore': False}
    }

    request = await auction_stub.get_request()
    assert request.data == {'announcementsIds': [173975523]}


async def test_v1_get_offer_duplicates_desktop_public__tab_all__offers_found__200(http, pg, auction_mock):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers_similar_tab_all.sql')
    await pg.execute(
        'INSERT INTO offers_similars_flat(offer_id, deal_type, sort_date, group_id) '
        'VALUES(236308049, \'sale\', \'2020-08-10\', 236308049)'
    )
    await pg.execute(
        'INSERT INTO offers_similars_flat(offer_id, deal_type, sort_date, group_id) '
        'VALUES(236213060, \'sale\', \'2020-08-10\', 236308049)'
    )
    await pg.execute(
        'INSERT INTO offers_similars_flat(offer_id, deal_type, sort_date, group_id) '
        'VALUES(236331615, \'sale\', \'2020-08-10\', 236308049)'
    )
    await pg.execute(
        'INSERT INTO offers_similars_flat(offer_id, deal_type, sort_date, group_id) '
        'VALUES(233353644, \'sale\', \'2020-08-10\', 236308049)'
    )
    await pg.execute(
        'INSERT INTO offers_similars_flat(offer_id, deal_type, sort_date, group_id) '
        'VALUES(177300443, \'sale\', \'2020-08-10\', 236308049)'
    )

    # act
    response = await http.request(
        'POST',
        '/public/v1/get-offers-duplicates-for-desktop/',
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
                'auctionBet': None,
                'displayDate': '2020-07-08T12:28:46.727000+00:00',
                'geo': {
                    'address': [
                        'Краснодарский край',
                        'Сочи',
                        'Макаренко мкр',
                        'улица Ботаническая',
                        '34'
                    ],
                    'underground': None},
                'mainPhotoUrl': 'https://cdn-p.cian.site/images/3/572/154/'
                                'kvartira-makarenko-botanicheskaya-ulica-451275372-2.jpg',
                'offerId': 177300443,
                'priceInfo': {'exact': '25\xa0000\xa0₽/мес.', 'range': None},
                'title': '1-комн.\xa0кв., 33\xa0м², 4/7\xa0этаж',
                'type': 'duplicate',
                'url': 'http://master.dev3.cian.ru/rent/flat/177300443',
                'vas': []
            }
        ],
        'page': {'canLoadMore': False, 'count': 4, 'pageCount': 2}}


async def test_v1_get_offer_duplicates_desktop_public__tab_all__duplicates__not_found__200(http, pg, auction_mock):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')

    # act
    response = await http.request(
        'POST',
        '/public/v1/get-offers-duplicates-for-desktop/',
        json={'offerId': 231655140, 'type': 'all'},
        headers={'X-Real-UserId': 47135244},
    )

    # assert
    assert response.data == {'offers': [], 'page': {'canLoadMore': False, 'count': 0, 'pageCount': 0}}
