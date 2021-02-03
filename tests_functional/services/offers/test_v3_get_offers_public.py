from pathlib import Path


async def test_v3_get_offers_public__search_text__result(http, pg):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')

    # act
    response = await http.request(
        'POST',
        '/public/v3/get-offers/',
        json={
            'filters': {
                'statusTab': 'active',
                'searchText': '+7 (962) 078 83-57 Красноярский край'
            }
        },
        headers={
            'X-Real-UserId': 29437831
        },
    )

    # assert
    assert response.data['offers'][0]['id'] == 209194477


async def test_v3_get_offers_private__search_text__result(http, pg):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')

    # act
    response = await http.request(
        'POST',
        '/v3/get-offers/',
        json={
            'filters': {
                'statusTab': 'active',
                'searchText': '+7 (962) 078 83-57 Красноярский край'
            },
            'userId': 29437831,
        },
    )

    # assert
    assert response.data['offers'][0]['id'] == 209194477
