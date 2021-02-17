async def test_v1_get_offers_mobile_public__200(http, pg):
    # act
    response = await http.request(
        'POST',
        '/public/v1/get-my-offers-mobile/',
        headers={
            'X-Real-UserId': 29437831
        },
        json={
            'limit': 20,
            'offset': 0,
            'tabType': 'inactive',
            'search': 'test_search_text',
            'filters': {
                'dealType': 'sale',
                'offerType': 'suburban',
            }
        }
    )

    # assert
    assert response.data == {
        'offers': [
            {'archivedDate': '2020-12-14T22:44:57.890178+00:00',
             'auction': {
                 'concurrencyTypeTitle': 'concurrency_type_title',
                 'concurrencyTypes': ['concurrencyTypes'],
                 'currentBet': 5.1,
                 'increaseBetsPositionsCount': 2,
                 'isActive': True,
                 'isAvailableAuction': True,
                 'isFixedBet': False,
                 'isStrategyEnabled': True,
                 'name': 'name',
                 'noteBet': 'note_bet',
                 'strategyDescription': 'strategy_description',
                 'type': 'type'
             },
             'availableActions': {
                 'canChangePublisher': True,
                 'canDelete': True,
                 'canEdit': True,
                 'canMoveToArchive': True,
                 'canRaise': True,
                 'canRaiseWithoutAddform': True,
                 'canRestore': True,
                 'canUpdateEditDate': True,
                 'canViewSimilarOffers': True
             },
             'category': 'flatSale',
             'complaints': [{
                 'comment': 'comment',
                 'date': '2020-12-11T22:44:57.890178+00:00',
                 'decline': True,
                 'id': 1,
                 'reasonText': 'reason_text'
             }],
             'deactivatedService': {
                 'description': 'description',
                 'isAutoRestoreOnPaymentEnabled': True},
             'dealType': 'sale',
             'description': 'тестовое описание замоканного объявления',
             'formattedAddress': 'formatted_address',
             'formattedInfo': 'formatted_info',
             'formattedPrice': '9\xa0900\xa0000₽',
             'hasPhotoOffence': False,
             'hasVideoOffence': False,
             'identificationPending': False,
             'isArchived': False,
             'isAuction': True,
             'isObjectOnPremoderation': False,
             'offerId': 36298746,
             'offerType': 'flat',
             'photo': 'https://cdn-p.cian.site/images/3/267/099/kvartira-moskva-golubinskaya-ulica-990762376-2.jpg',
             'price': {'currency': 'rur', 'value': 9900000.0},
             'publishTillDate': '2020-12-10 22:44:57.890178+00:00',
             'services': ['auction', 'premium'],
             'stats': {
                 'callsCount': 999,
                 'competitorsCount': 100,
                 'dailyViews': 99,
                 'duplicatesCount': 10,
                 'favorites': 5,
                 'skippedCallsCount': 1,
                 'totalViews': 1111
             },
             'status': 'Published'
             }
        ],
        'page': {'canLoadMore': False, 'limit': 20, 'offset': 0}
    }
