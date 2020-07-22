from pathlib import Path


async def test_v2_get_offer_tabs_public__duplicates_found__200(http_client, pg, auction_mock):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')
    await pg.execute('INSERT INTO offers_duplicates values(231655140, 231655140, \'2020-05-26\')')
    await pg.execute('INSERT INTO offers_duplicates values(231659418, 231655140, \'2020-05-26\')')
    await pg.execute('INSERT INTO offers_duplicates values(173975523, 231655140, \'2020-05-26\')')

    # act
    response = await http_client.request(
        'POST',
        '/public/v1/get-offer-duplicates-tabs/',
        json={'offerId': 231655140},
        headers={'X-Real-UserId': 47135244},
    )

    # assert
    assert response.data == {
        'tabs': [
            {'title': 'Все', 'type': 'all', 'count': 2},
            {'title': 'Дубли', 'type': 'duplicate', 'count': 2},
        ]
    }


async def test_v2_get_offer_tabs_public__duplicates_not_found__200(http_client, pg):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')

    # act
    response = await http_client.request(
        'POST',
        '/public/v1/get-offer-duplicates-tabs/',
        json={'offerId': 231655140},
        headers={'X-Real-UserId': 47135244},
    )

    # assert
    assert response.data == {'tabs': []}


async def test_v2_get_offer_tab_public__not_validate_offer__200(http_client, pg):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')

    # act
    response = await http_client.request(
        'POST',
        '/public/v1/get-offer-duplicates-tabs/',
        json={'offerId': 209194477},
        headers={'X-Real-UserId': 29437831},
    )

    # assert
    assert response.data == {'tabs': []}


async def test_v2_get_offers_tabs_public__offer_not_found__400(http_client):
    # act
    response = await http_client.request(
        'POST',
        '/public/v1/get-offer-duplicates-tabs/',
        json={'offerId': 165491301},
        headers={'X-Real-UserId': 1111},
        expected_status=400,
    )

    # assert
    assert response.data['errors'][0]['code'] == 'notFound'
