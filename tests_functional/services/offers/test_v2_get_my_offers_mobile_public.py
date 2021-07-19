from pathlib import Path


async def test_get_by_search_text__return_expected_result(http, pg):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')

    # act
    response = await http.request(
        'POST',
        '/public/v2/get-my-offers-mobile/',
        json={
            'limit': 10,
            'offset': 0,
            'tabType': 'sale',
            'search': '+7 (962) 078 83-57 Асфальтовая дорога',
        },
        headers={
            'X-Real-UserId': 29437831
        },
    )

    # assert
    assert response.data == {
        'offers': [
            {
                'archivedDate': None,
                'auction': None,
                'availableActions': {
                    'canChangePublisher': False,
                    'canDelete': False,
                    'canEdit': False,
                    'canMoveToArchive': False,
                    'canRaise': False,
                    'canRaiseWithoutAddform': False,
                    'canRestore': False,
                    'canUpdateEditDate': False,
                    'canViewSimilarOffers': False,
                },
                'category': 'landSale',
                'cianId': 209194477,
                'cianUserId': 29437831,
                'complaints': None,
                'coworkingId': None,
                'deactivatedService': None,
                'dealType': 'sale',
                'description': (
                    'Продается участок в КП Времена года, 14.93 сот. '
                    'Коттеджный поселок "времена года" запроектирован '
                    'на самом популярном и экологичном загородном '
                    'направлении: нулевой километр на выезде из города '
                    'со стороны поста дпс "бугач" в сторону аэропорта. '
                    'Поселок хорошо вписан в природное окружение.\n'
                    'Поселок расположен в абсолютной транспортной '
                    'доступности и близости к городу, в автомобильной '
                    'развязке федеральных автодорог. вы можете, минуя '
                    'пробки, быстро попасть в город по любому из '
                    'четырех въездов (бугач, брянская, северный, '
                    'авиаторов). КП располагает благоприятными '
                    'условиями для спокойной семейной жизни и отдыха '
                    'на природе.\n'
                    'Асфальтовая дорога к въездной группе поселка есть '
                    'уже сегодня, и уже сегодня она открыта для '
                    'проезда (чистится) круглый год.'
                ),
                'formattedAddress': (
                    'Красноярский край, Емельяновский район, пос. '
                    'Солонцы, Времена Года ДНП'
                ),
                'formattedInfo': 'Земельный участок • 14.93\xa0сот.',
                'formattedPrice': '2\xa0594\xa0400\xa0₽',
                'hasPhotoOffence': False,
                'hasVideoOffence': False,
                'identificationPending': False,
                'isArchived': False,
                'isAuction': False,
                'isDeclined': False,
                'isObjectOnPremoderation': False,
                'isPrivateAgent': True,
                'offerId': 209194477,
                'offerType': 'suburban',
                'photo': 'https://cdn-p.cian.site/images/1/138/977/779831175-2.jpg',
                'price': {'currency': 'rur', 'value': 2594400.0},
                'publishTillDate': None,
                'realtyUserId': 29437831,
                'services': ['paid'],
                'stats': {
                    'callsCount': None,
                    'competitorsCount': None,
                    'dailyViews': 0,
                    'duplicatesCount': None,
                    'favorites': None,
                    'skippedCallsCount': None,
                    'totalViews': 0,
                },
                'status': 'published',
            },
        ],
        'page': {
            'canLoadMore': False,
            'limit': 10,
            'offset': 0,
        }
    }
