import os

from tests_functional.utils import load_data


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
    await pg.execute(load_data(os.path.dirname(__file__) + '/../../', 'offers.sql'))

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
    await pg.execute(load_data(os.path.dirname(__file__) + '/../../', 'offers.sql'))

    # act
    response = await http_client.request(
        'POST',
        '/public/v1/get-offer-duplicates/',
        json={'offerId': 231655140, 'type': 'all'},
        headers={'X-Real-UserId': 47135244},
    )

    # assert
    assert len(response.data['offers']) == 0


async def test_v2_get_offers_public__duplicates_found__200(http_client, pg):
    # arrange
    await pg.execute(load_data(os.path.dirname(__file__) + '/../../', 'offers.sql'))
    await pg.execute('INSERT INTO offers_duplicates values(231655140, 231655140, \'2020-05-09\')')
    await pg.execute('INSERT INTO offers_duplicates values(231659418, 231655140, \'2020-05-09\')')

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
                'vas': ['payed'],
                'priceInfo': {'range': None, 'exact': '1 550 000 ₽'},
                'properties': ['2-комн. кв.', '59 м²', '3/3 этаж'],
                'geo': {
                    'underground': None,
                    'newbuilding': None,
                    'address': ['Свердловская область', 'Нижний Тагил', 'улица Циолковского', '37/50']
                },
                'offerId': 231659418,
                'type': 'duplicate',
                'displayDate': '2020-05-09T10:06:29.159746+00:00',
                'mainPhotoUrl': 'https://cdn-p.cian.site/images/6/179/378/'
                                'kvartira-nizhniy-tagil-ulica-ciolkovskogo-873971625-3.jpg',
                'auctionBet': None
            }
        ],
        'page': {'pageCount': 1, 'count': 1, 'canLoadMore': False},
        'tabs': [{'type': 'all', 'title': 'Все', 'count': 1}, {'type': 'duplicate', 'title': 'Дубли', 'count': 1}]
    }
