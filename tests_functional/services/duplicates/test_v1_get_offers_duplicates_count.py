from pathlib import Path


async def test_v1_get_offers_duplicates_count(http, pg):
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

    # act
    response = await http.request(
        'POST',
        '/v1/get-offers-duplicates-count/',
        json={'offerIds': [231655140]},
    )

    # assert
    assert response.data['data'] == [{'competitorsCount': 2, 'duplicatesCount': 2, 'offerId': 231655140}]


async def test_v1_get_offers_duplicates_count__emty__empty(http, pg):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')
    await pg.execute('INSERT INTO offers_duplicates values(231655140, 231655140, \'2020-05-09\')')
    await pg.execute('INSERT INTO offers_duplicates values(173975523, 231655140, \'2020-05-09\')')

    # act
    response = await http.request(
        'POST',
        '/v1/get-offers-duplicates-count/',
        json={'offerIds': []},
    )

    # assert
    assert response.data['data'] == []


async def test_v1_get_offers_duplicates_count__offer_not_found__response(http, pg):
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

    # act
    response = await http.request(
        'POST',
        '/v1/get-offers-duplicates-count/',
        json={'offerIds': [111]},
    )

    # assert
    assert response.data['data'] == []
