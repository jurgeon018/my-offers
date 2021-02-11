from pathlib import Path


async def test_v1_get_offers_mobile_public__200(http, pg):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')

    # act
    response = await http.request(
        'POST',
        '/public/v1/get-offers-counters-mobile/',
        headers={
            'X-Real-UserId': 29437831
        },
        json={'search': 'test_search'}
    )

    # assert
    assert response.data == {
        'rent': {'commercial': 342, 'flat': 233, 'suburban': 3423, 'total': 3998},
        'sale': {'commercial': 343, 'flat': 234, 'suburban': 3424, 'total': 4001},
        'archieved': {'rent': 232, 'sale': 3422, 'total': 3654},
        'inactive': {'rent': 1, 'sale': 2, 'total': 3},
    }
