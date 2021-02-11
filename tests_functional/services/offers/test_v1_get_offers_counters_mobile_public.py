from pathlib import Path


async def test_v1_get_offers_public__search_text__result(http, pg):
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
        'archieved': {'commercial': 341, 'flat': 232, 'suburban': 3422, 'total': 3995},
        'inactive': {'commercial': 3, 'flat': 1, 'suburban': 2, 'total': 6},
    }
