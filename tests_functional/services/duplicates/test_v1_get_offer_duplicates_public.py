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
        'VALUES(173975523, \'sale\', \'2020-08-11\', 231655140)'
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
        'tabs': [{'title': 'Все', 'type': 'all', 'count': 2},
                 {'title': 'Дубли', 'type': 'duplicate', 'count': 2}]
    }

    request = await auction_stub.get_request()
    assert request.data == {'announcementsIds': [173975523]}


async def test_v2_get_offers_public__whithout_type_parameter(http, pg, auction_mock):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')
    await pg.execute(
        'INSERT INTO offers_similars_flat(offer_id, deal_type, sort_date, group_id) '
        'VALUES(231655140, \'sale\', \'2020-08-10\', 231655140)'
    )
    await pg.execute(
        'INSERT INTO offers_similars_flat(offer_id, deal_type, sort_date, group_id) '
        'VALUES(173975523, \'sale\', \'2020-08-10\', 231655140)'
    )

    # act
    response = await http.request(
        'POST',
        '/public/v1/get-offer-duplicates/',
        json={'offerId': 231655140},
        headers={'X-Real-UserId': 47135244},
    )

    # assert
    assert len(response.data['offers']) == 1


async def test_v2_get_offers_public__simimar_tab__result(http, pg, auction_mock):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')
    await pg.execute(
        'INSERT INTO offers_similars_flat(offer_id, deal_type, sort_date, district_id, price, rooms_count) '
        'VALUES(231655140, \'sale\', \'2020-08-10\', 231655140, 100, 2)'
    )
    await pg.execute(
        'INSERT INTO offers_similars_flat(offer_id, deal_type, sort_date, district_id, price, rooms_count) '
        'VALUES(173975523, \'sale\', \'2020-08-10\', 231655140, 100, 2)'
    )

    # act
    response = await http.request(
        'POST',
        '/public/v1/get-offer-duplicates/',
        json={'offerId': 231655140, 'type': 'similar'},
        headers={'X-Real-UserId': 47135244},
    )

    # assert
    assert len(response.data['offers']) == 1


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
