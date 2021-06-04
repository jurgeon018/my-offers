from pathlib import Path


async def test_v1_get_offers_counters_mobile_public__200(http, pg):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')

    # act
    response = await http.request(
        'POST',
        '/public/v2/get-offers-counters-mobile/',
        headers={
            'X-Real-UserId': 29437831
        },
        json={}
    )

    # assert
    assert response.data == {
        'archived': {'rent': 0, 'sale': 0, 'total': 0},
        'declined': {'rent': 0, 'sale': 0, 'total': 0},
        'inactive': {'rent': 0, 'sale': 0, 'total': 0},
        'rent': {'commercial': 0, 'flat': 0, 'suburban': 0, 'total': 0},
        'sale': {'commercial': 0, 'flat': 0, 'suburban': 1, 'total': 1}
    }


async def test_v1_get_offers_counters_mobile_public__search__200(http, pg):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')

    # act
    response = await http.request(
        'POST',
        '/public/v2/get-offers-counters-mobile/',
        headers={
            'X-Real-UserId': 29437831
        },
        json={'search': 'test_search'}
    )

    # assert
    assert response.data == {
        'archived': {'rent': 0, 'sale': 0, 'total': 0},
        'declined': {'rent': 0, 'sale': 0, 'total': 0},
        'inactive': {'rent': 0, 'sale': 0, 'total': 0},
        'rent': {'commercial': 0, 'flat': 0, 'suburban': 0, 'total': 0},
        'sale': {'commercial': 0, 'flat': 0, 'suburban': 0, 'total': 0}
    }


async def test_v1_get_offers_counters_mobile_public__200__wrong_user_id(http, pg):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')

    # act
    response = await http.request(
        'POST',
        '/public/v2/get-offers-counters-mobile/',
        headers={
            'X-Real-UserId': 11111
        },
        json={'search': 'test_search'}
    )

    # assert
    assert response.data == {
        'archived': {'rent': 0, 'sale': 0, 'total': 0},
        'declined': {'rent': 0, 'sale': 0, 'total': 0},
        'inactive': {'rent': 0, 'sale': 0, 'total': 0},
        'rent': {'commercial': 0, 'flat': 0, 'suburban': 0, 'total': 0},
        'sale': {'commercial': 0, 'flat': 0, 'suburban': 0, 'total': 0}
    }
