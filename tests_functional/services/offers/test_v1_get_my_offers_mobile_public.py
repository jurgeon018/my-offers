import asyncio
from pathlib import Path

import pytest
from cian_functional_test_utils.pytest_plugin import MockResponse


@pytest.fixture(name='mobile_offers_integrations_mock')
async def _integration_mock(moderation_mock, moderation_checks_orchestrator_mock, auction_mock):
    await asyncio.gather(
        moderation_mock.add_stub(
            method='POST',
            path='/v1/get-video-offences-for-announcements/',
            response=MockResponse(
                body={
                    'items': [
                        {
                            'announcementId': 0,
                            'title': 'string',
                            'comment': 'string',
                            'videoIds': [
                                'string'
                            ]
                        }
                    ]
                }
            ),
        ),
        moderation_mock.add_stub(
            method='POST',
            path='/v1/get-image-offences-for-announcements/',
            response=MockResponse(
                body={
                    'items': [
                        {
                            'announcementId': 0,
                            'title': 'string',
                            'comment': 'string',
                            'imageIds': [
                                0
                            ]
                        }
                    ]
                }
            ),
        ),
        moderation_checks_orchestrator_mock.add_stub(
            method='POST',
            path='/v1/check-users-need-identification/',
            response=MockResponse(
                body=[
                    {
                        'userId': 29437831,
                        'identificationStatus': 'okNoIdentificationNeeded',
                        'objectIds': [
                            0
                        ]
                    }
                ]
            ),
        ),
        auction_mock.add_stub(
            method='GET',
            path='/v1/get-announcements-info-for-mobile/',
            response=MockResponse(
                body={
                    'announcements': [
                        {
                            'announcementId': 0,
                            'concurrencyTypeTitle': 'string',
                            'increaseBetsPositionsCount': 0,
                            'currentBet': 0,
                            'noteBet': 'string',
                            'isAvailableAuction': True,
                            'concurrencyTypes': [
                                {
                                    'type': 'region',
                                    'name': 'string',
                                    'isActive': True
                                }
                            ],
                            'serpPosition': 0,
                            'isStrategyEnabled': True,
                            'isFixedBet': True,
                            'strategyDescription': 'string',
                            'betPositionInfo': 'string'
                        }
                    ]
                }
            ),
        )
    )


async def test_v1_get_offers_mobile_public__200(http, pg, mobile_offers_integrations_mock):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')

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
            'tabType': 'sale',
            'filters': {
                'dealType': 'sale',
                'offerType': 'suburban',
            }
        }
    )

    # assert
    # TODO: CD-100663, CD-100665
    assert response.data == {
        'offers': [
            {'archivedDate': '2020-12-14T22:44:57.890178+00:00',
             'auction': {
                 'concurrencyTypeTitle': 'concurrency_type_title',
                 'concurrencyTypes': [{
                     'isActive': True,
                     'name': 'name',
                     'type': 'type'
                 }],
                 'currentBet': 5.1,
                 'increaseBetsPositionsCount': 2,
                 'isAvailableAuction': True,
                 'isFixedBet': False,
                 'isStrategyEnabled': True,
                 'noteBet': 'note_bet',
                 'strategyDescription': 'strategy_description',
             },
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
             'category': 'flatSale',
             'complaints': [{
                 'comment': 'comment',
                 'date': '2020-12-11T22:44:57.890178+00:00',
                 'id': 1,
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
             'coworkingId': 123,
             'isPrivateAgent': True,
             'stats': {
                 'callsCount': 999,
                 'competitorsCount': None,
                 'dailyViews': 99,
                 'duplicatesCount': None,
                 'favorites': None,
                 'skippedCallsCount': 1,
                 'totalViews': None,
             },
             'status': 'published'
             }
        ],
        'page': {'canLoadMore': False, 'limit': 20, 'offset': 0}
    }


async def test_v1_get_offers_mobile_public__200__empty_offers(http, pg, mobile_offers_integrations_mock):
    # arrange

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
            'tabType': 'sale',
            'filters': {
                'dealType': 'sale',
                'offerType': 'suburban',
            }
        }
    )

    # assert
    assert response.data == {
        'offers': [],
        'page': {'canLoadMore': False, 'limit': 20, 'offset': 0}
    }


async def test_v1_get_offers_mobile_public__200__can_load_more(http, pg, mobile_offers_integrations_mock):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers_for_pagination.sql')

    # act
    response = await http.request(
        'POST',
        '/public/v1/get-my-offers-mobile/',
        headers={
            'X-Real-UserId': 29437831
        },
        json={
            'limit': 1,
            'offset': 0,
            'tabType': 'sale',
            'filters': {
                'dealType': 'sale',
                'offerType': 'suburban',
            }
        }
    )

    # assert
    # TODO: CD-100663, CD-100665
    assert response.data == {
        'offers': [
            {'archivedDate': '2020-12-14T22:44:57.890178+00:00',
             'auction': {
                 'concurrencyTypeTitle': 'concurrency_type_title',
                 'concurrencyTypes': [{
                     'isActive': True,
                     'name': 'name',
                     'type': 'type'
                 }],
                 'currentBet': 5.1,
                 'increaseBetsPositionsCount': 2,
                 'isAvailableAuction': True,
                 'isFixedBet': False,
                 'isStrategyEnabled': True,
                 'noteBet': 'note_bet',
                 'strategyDescription': 'strategy_description',
             },
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
             'category': 'flatSale',
             'complaints': [{
                 'comment': 'comment',
                 'date': '2020-12-11T22:44:57.890178+00:00',
                 'id': 1,
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
             'coworkingId': 123,
             'isPrivateAgent': True,
             'stats': {
                 'callsCount': 999,
                 'competitorsCount': None,
                 'dailyViews': 99,
                 'duplicatesCount': None,
                 'favorites': None,
                 'skippedCallsCount': 1,
                 'totalViews': None,
             },
             'status': 'published'
             }
        ],
        'page': {'canLoadMore': True, 'limit': 1, 'offset': 0}
    }
