import os

from tests_functional.utils import load_data


async def test_v1_get_offers_duplicates_count(http_client, pg):
    # arrange
    await pg.execute(load_data(os.path.dirname(__file__) + '/../../', 'offers.sql'))
    await pg.execute('INSERT INTO offers_duplicates values(231655140, 231655140, \'2020-05-09\')')
    await pg.execute('INSERT INTO offers_duplicates values(173975523, 231655140, \'2020-05-09\')')

    # act
    response = await http_client.request(
        'POST',
        '/v1/get-offers-duplicates-count/',
        json={'offerIds': [231655140, 173975523, 1111]},
    )

    # assert
    assert response.data['data'] == [
        {'duplicatesCount': 1, 'offerId': 173975523, 'competitorsCount': 0},
        {'duplicatesCount': 1, 'offerId': 231655140, 'competitorsCount': 0}
    ]


async def test_v1_get_offers_duplicates_count__emty__empty(http_client, pg):
    # arrange
    await pg.execute(load_data(os.path.dirname(__file__) + '/../../', 'offers.sql'))
    await pg.execute('INSERT INTO offers_duplicates values(231655140, 231655140, \'2020-05-09\')')
    await pg.execute('INSERT INTO offers_duplicates values(173975523, 231655140, \'2020-05-09\')')

    # act
    response = await http_client.request(
        'POST',
        '/v1/get-offers-duplicates-count/',
        json={'offerIds': []},
    )

    # assert
    assert response.data['data'] == []
