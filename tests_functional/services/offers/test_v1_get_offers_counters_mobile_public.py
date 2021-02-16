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
        'sale': {'commercial': 0, 'suburban': 1, 'total': 1, 'flat': 0},
        'rent': {'commercial': 0, 'suburban': 0, 'total': 0, 'flat': 0},
        'archived': {'sale': 0, 'rent': 0, 'total': 0},
        'inactive': {'sale': 0, 'rent': 0, 'total': 0},
    }


async def test_v1_get_offers_mobile_public__200__degradation_wrong_user_id(http, pg):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')

    # act
    response = await http.request(
        'POST',
        '/public/v1/get-offers-counters-mobile/',
        headers={
            'X-Real-UserId': 11111
        },
        json={'search': 'test_search'}
    )

    # assert
    assert response.data == {
        'archived': {'rent': 0, 'sale': 0, 'total': 0},
        'inactive': {'rent': 0, 'sale': 0, 'total': 0},
        'rent': {'commercial': 0, 'flat': 0, 'suburban': 0, 'total': 0},
        'sale': {'commercial': 0, 'flat': 0, 'suburban': 0, 'total': 0},
    }


async def test_v1_get_offers_mobile_public__200__degradation_exception(http, pg, runtime_settings):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')
    await runtime_settings.set({'DB_SLOW_TIMEOUT': 0})

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
        'archived': None,
        'inactive': None,
        'rent': None,
        'sale': None,
    }
