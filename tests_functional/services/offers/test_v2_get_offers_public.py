from pathlib import Path


async def test_v2_get_offers_public__not_found__200(http_client):
    # act
    response = await http_client.request(
        'POST',
        '/public/v2/get-offers/',
        json={
            'filters': {
                'statusTab': 'active',
                'searchText': '+7 (929) 444 55-77 Москва'
            }
        },
        headers={
            'X-Real-UserId': 13933440
        },
    )

    # assert
    assert len(response.data['offers']) == 0


async def test_v2_get_offers_public__search_text__result(http_client, pg):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')

    # act
    response = await http_client.request(
        'POST',
        '/public/v2/get-offers/',
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
