from pathlib import Path


async def test_v3_get_offers_public__search_text__result(http, pg):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')

    # act
    response = await http.request(
        'GET',
        '/public/v1/get-offers-counters/',
        headers={
            'X-Real-UserId': 29437831
        },
    )

    # assert
    assert response.data == {'declined': 0, 'archived': None, 'active': 1, 'notActive': 0}
