from pathlib import Path


async def test_get_offers_for_calltracking(http, pg):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')

    # act
    response = await http.request(
        'POST',
        '/v1/get-offers-for-calltracking/',
        json={'offerIds': [221798834, 227140265, 1]},
    )

    # assert
    assert response.data == {
        'offers': [
            {'mainPhotoUrl': 'https://cdn-p.cian.site/images/4/755/838/838557466-2.jpg', 'offerId': 227140265},
            {'mainPhotoUrl': 'https://cdn-p.cian.site/images/0/312/787/787213051-2.jpg', 'offerId': 221798834}
        ]
    }


async def test_get_offers_for_calltracking_card(http, pg):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')

    # act
    response = await http.request(
        'POST',
        '/v1/get-offers-for-calltracking-card/',
        json={'offerIds': [221798834, 227140265, 1]},
    )

    # assert
    assert response.data == {
        'offers': [
            {
                'dealType': 'sale',
                'geo': {
                    'address': ['Санкт-Петербург', 'шоссе Суздальское'],
                    'underground': {
                        'lineColor': '087DCD',
                        'name': 'Озерки',
                        'regionId': 2
                    }
                },
                'mainPhotoUrl': 'https://cdn-p.cian.site/images/4/755/838/838557466-2.jpg',
                'offerId': 227140265,
                'properties': ['1-комн.\xa0кв.', '33\xa0м²', '1/15\xa0этаж'],
                'offerType': 'flat',
            },
            {
                'dealType': 'sale',
                'geo': {
                    'address': ['Самарская область', 'Волжский район', 'Лопатино с/пос', 'пос. Самарский'],
                    'underground': None
                },
                'mainPhotoUrl': 'https://cdn-p.cian.site/images/0/312/787/787213051-2.jpg',
                'offerId': 221798834,
                'properties': ['Земельный участок', '10.0\xa0сот.'],
                'offerType': 'suburban',
            }
        ],
    }
