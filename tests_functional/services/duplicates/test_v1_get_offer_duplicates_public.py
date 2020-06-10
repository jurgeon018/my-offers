from pathlib import Path

from cian_functional_test_utils.pytest_plugin import MockResponse


async def test_v2_get_offers_public__offer_not_found__400(http_client):
    # act
    response = await http_client.request(
        'POST',
        '/public/v1/get-offer-duplicates/',
        json={'offerId': 165491301, 'type': 'all'},
        headers={'X-Real-UserId': 1111},
        expected_status=400,
    )

    # assert
    assert response.data['errors'][0]['code'] == 'notFound'


async def test_v2_get_offers_public__bad_offer__200(http_client, pg):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')

    # act
    response = await http_client.request(
        'POST',
        '/public/v1/get-offer-duplicates/',
        json={'offerId': 209194477, 'type': 'all'},
        headers={'X-Real-UserId': 29437831},
    )

    # assert
    assert len(response.data['offers']) == 0


async def test_v2_get_offers_public__duplicates_not_found__200(http_client, pg):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')

    # act
    response = await http_client.request(
        'POST',
        '/public/v1/get-offer-duplicates/',
        json={'offerId': 231655140, 'type': 'all'},
        headers={'X-Real-UserId': 47135244},
    )

    # assert
    assert len(response.data['offers']) == 0


async def test_v2_get_offers_public__duplicates_found__200(http_client, pg, auction_mock):
    # arrange
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
    response = await http_client.request(
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


async def test_v2_get_offers_public__whithout_type_parameter(http_client, pg, auction_mock):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')
    await pg.execute('INSERT INTO offers_duplicates values(231655140, 231655140, \'2020-05-09\')')
    await pg.execute('INSERT INTO offers_duplicates values(173975523, 231655140, \'2020-05-09\')')

    # act
    response = await http_client.request(
        'POST',
        '/public/v1/get-offer-duplicates/',
        json={'offerId': 231655140},
        headers={'X-Real-UserId': 47135244},
    )

    # assert
    assert len(response.data['offers']) == 1
