import asyncio
from datetime import datetime, timedelta
from pathlib import Path

import pytest
import pytz
from cian_functional_test_utils.helpers import ANY
from cian_functional_test_utils.pytest_plugin import MockResponse


@pytest.fixture(name='mobile_offers_integrations_mock')
async def _integration_mock(
        moderation_mock,
        moderation_checks_orchestrator_mock,
        auction_mock,
        search_offers_mock,
        callbook_mock,
):
    await asyncio.gather(
        callbook_mock.add_stub(
            method='POST',
            path='/v1/get-user-calls-by-offers-totals/',
            response=MockResponse(
                body={
                    'data': [
                        {
                            'callsCount': 10,
                            'missedCallsCount': 9,
                            'offerId': 209194477,
                        }
                    ]
                }
            ),
        ),
        moderation_mock.add_stub(
            method='POST',
            path='/v1/get-video-offences-for-announcements/',
            response=MockResponse(
                body={
                    'items': [
                        {
                            'announcementId': 209194477,
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
        search_offers_mock.add_stub(
            method='POST',
            path='/v1/enrich-offers-with-formatted-fields/',
            response=MockResponse(
                body={
                    'formattedData': [
                        {
                            'fields': {
                                'formattedAdditionalExtraInfo': 'string',
                                'formattedAdditionalInfo': 'string',
                                'formattedAdditionalPrice': 'string',
                                'formattedAddress': 'string',
                                'formattedAreaParts': [
                                    {
                                        'area': 'string',
                                        'price': 'string',
                                        'pricePerMeter': 'string'
                                    }
                                ],
                                'formattedCardInfo': 'string',
                                'formattedCommunalInfo': 'string',
                                'formattedFullInfo': 'string',
                                'formattedFullPrice': 'string',
                                'formattedPremisesInfo': 'string',
                                'formattedPricePerMeter': 'string',
                                'formattedShortInfo': 'string',
                                'formattedShortPrice': 'string',
                                'formattedVatType': 'string'
                            },
                            'id': 209194477
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
                            'announcementId': 209194477,
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
                            'announcementId': 209194477,
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


async def test_v1_get_offers_mobile_public__load_sale_offers__offers_data(
        http,
        pg,
        mobile_offers_integrations_mock,
        cassandra_statistics,
):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'agents_hiearachy.sql')
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers_offences.sql')
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers_premoderations.sql')

    date = datetime.now(tz=pytz.UTC)
    await cassandra_statistics.execute(
        """
            update
                views_current
            set
                views = views + 22
            where
                offer_id = 209194477 and
                year = %s and
                month = %s and
                day = %s
        """,
        [
            date.year,
            date.month,
            date.day,
        ]
    )

    date = datetime.now(tz=pytz.UTC) - timedelta(days=1)
    await cassandra_statistics.execute(
        """
            update
                views_total
            set
                views_total = 80
            where
                offer_id = 209194477 and
                year = %s and
                month = %s and
                day = %s
        """,
        [
            date.year,
            date.month,
            date.day,
        ]
    )

    # act
    response = await http.request(
        'POST',
        '/public/v2/get-my-offers-mobile/',
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

    assert response.data == {'offers': [
        {
            'archivedDate': None,
            'auction': {
                'concurrencyTypeTitle': 'string',
                'concurrencyTypes': [
                    {'isActive': True,
                     'name': 'string',
                     'type': 'region'
                     }
                ],
                'currentBet': 0.0,
                'increaseBetsPositionsCount': 0,
                'isAvailableAuction': True,
                'isFixedBet': True,
                'isStrategyEnabled': True,
                'noteBet': 'string',
                'strategyDescription': 'string'
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
                'canViewSimilarOffers': False
            },
            'category': 'landSale',
            'cianUserId': 29437831,
            'complaints': None,
            'isDeclined': False,
            'coworkingId': None,
            'deactivatedService': None,
            'dealType': 'sale',
            'description': ANY,
            'formattedAddress': '???????????????????????? ????????, ?????????????????????????? ??????????, ??????. '
                                '??????????????, ?????????????? ???????? ??????',
            'formattedInfo': '?????????????????? ?????????????? ??? 14.93\xa0??????.',
            'formattedPrice': '2\xa0594\xa0400\xa0???',
            'hasPhotoOffence': False,
            'hasVideoOffence': False,
            'identificationPending': False,
            'isArchived': False,
            'isAuction': False,
            'isObjectOnPremoderation': False,
            'isPrivateAgent': True,
            'offerId': 209194477,
            'cianId': 209194477,
            'offerType': 'suburban',
            'photo': 'https://cdn-p.cian.site/images/1/138/977/779831175-2.jpg',
            'price': {'currency': 'rur', 'value': 2594400.0},
            'publishTillDate': None,
            'realtyUserId': 29437831,
            'services': ['paid'],
            'stats': {
                'callsCount': 10,
                'competitorsCount': None,
                'dailyViews': 22,
                'duplicatesCount': None,
                'favorites': None,
                'skippedCallsCount': 9,
                'totalViews': 102,
            },
            'status': 'published'
        }
    ],
        'page': {'canLoadMore': False, 'limit': 20, 'offset': 0}
    }


async def test_v1_get_offers_mobile_public__load_offers_with_search_text__offers_data(
        http,
        pg,
        mobile_offers_integrations_mock,
        cassandra_statistics,
):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'agents_hiearachy.sql')
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers_offences.sql')
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers_premoderations.sql')

    date = datetime.now(tz=pytz.UTC)
    await cassandra_statistics.execute(
        """
            update
                views_current
            set
                views = views + 22
            where
                offer_id = 209194477 and
                year = %s and
                month = %s and
                day = %s
        """,
        [
            date.year,
            date.month,
            date.day,
        ]
    )

    date = datetime.now(tz=pytz.UTC) - timedelta(days=1)
    await cassandra_statistics.execute(
        """
            update
                views_total
            set
                views_total = 80
            where
                offer_id = 209194477 and
                year = %s and
                month = %s and
                day = %s
        """,
        [
            date.year,
            date.month,
            date.day,
        ]
    )

    # act
    response = await http.request(
        'POST',
        '/public/v2/get-my-offers-mobile/',
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
            },
            'search': '??????????????',
        }
    )

    assert response.data == {'offers': [
        {
            'archivedDate': None,
            'auction': {
                'concurrencyTypeTitle': 'string',
                'concurrencyTypes': [
                    {'isActive': True,
                     'name': 'string',
                     'type': 'region'
                     }
                ],
                'currentBet': 0.0,
                'increaseBetsPositionsCount': 0,
                'isAvailableAuction': True,
                'isFixedBet': True,
                'isStrategyEnabled': True,
                'noteBet': 'string',
                'strategyDescription': 'string'
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
                'canViewSimilarOffers': False
            },
            'category': 'landSale',
            'cianUserId': 29437831,
            'complaints': None,
            'isDeclined': False,
            'coworkingId': None,
            'deactivatedService': None,
            'dealType': 'sale',
            'description': ANY,
            'formattedAddress': '???????????????????????? ????????, ?????????????????????????? ??????????, ??????. '
                                '??????????????, ?????????????? ???????? ??????',
            'formattedInfo': '?????????????????? ?????????????? ??? 14.93\xa0??????.',
            'formattedPrice': '2\xa0594\xa0400\xa0???',
            'hasPhotoOffence': False,
            'hasVideoOffence': False,
            'identificationPending': False,
            'isArchived': False,
            'isAuction': False,
            'isObjectOnPremoderation': False,
            'isPrivateAgent': True,
            'offerId': 209194477,
            'cianId': 209194477,
            'offerType': 'suburban',
            'photo': 'https://cdn-p.cian.site/images/1/138/977/779831175-2.jpg',
            'price': {'currency': 'rur', 'value': 2594400.0},
            'publishTillDate': None,
            'realtyUserId': 29437831,
            'services': ['paid'],
            'stats': {
                'callsCount': 10,
                'competitorsCount': None,
                'dailyViews': 22,
                'duplicatesCount': None,
                'favorites': None,
                'skippedCallsCount': 9,
                'totalViews': 102,
            },
            'status': 'published'
        }
    ],
        'page': {'canLoadMore': False, 'limit': 20, 'offset': 0}
    }


async def test_v1_get_offers_mobile_public__load_inactive_offers__offers_data(
        http,
        pg,
        mobile_offers_integrations_mock,
):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offer_inactive.sql')
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers_offences.sql')
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers_premoderations.sql')

    # act
    response = await http.request(
        'POST',
        '/public/v2/get-my-offers-mobile/',
        headers={
            'X-Real-UserId': 29437831
        },
        json={
            'limit': 20,
            'offset': 0,
            'tabType': 'inactive',
            'filters': {
                'dealType': 'sale',
                'offerType': 'suburban',
            }
        }
    )

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
                    'canViewSimilarOffers': False
                },
                'category': 'landSale',
                'cianUserId': 29437831,
                'complaints': [
                    {
                        'comment': '???????????????? ???????????????? ???????????????? ????????????????',
                        'date': '2021-02-04T14:21:28.276339+00:00',
                        'id': 1833685,
                    }
                ],
                'isDeclined': False,
                'coworkingId': None,
                'deactivatedService': None,
                'dealType': 'sale',
                'description': ANY,
                'formattedAddress': '???????????????????????? ????????, ?????????????????????????? ??????????, ??????. '
                                    '??????????????, ?????????????? ???????? ??????',
                'formattedInfo': '?????????????????? ?????????????? ??? 14.93\xa0??????.',
                'formattedPrice': '2\xa0594\xa0400\xa0???',
                'hasPhotoOffence': True,
                'hasVideoOffence': True,
                'identificationPending': False,
                'isArchived': False,
                'isAuction': False,
                'isObjectOnPremoderation': True,
                'isPrivateAgent': True,
                'offerId': 209194477,
                'cianId': 209194477,
                'offerType': 'suburban',
                'photo': 'https://cdn-p.cian.site/images/1/138/977/779831175-2.jpg',
                'price': {'currency': 'rur', 'value': 2594400.0},
                'publishTillDate': None,
                'realtyUserId': 29437831,
                'services': ['paid'],
                'stats': {
                    'callsCount': None,
                    'competitorsCount': None,
                    'dailyViews': None,
                    'duplicatesCount': None,
                    'favorites': None,
                    'skippedCallsCount': None,
                    'totalViews': None
                },
                'status': 'published'
            }
        ],
        'page': {'canLoadMore': False, 'limit': 20, 'offset': 0}}


async def test_v1_get_offers_mobile_public__load_no_offers__empty_data(http, pg, mobile_offers_integrations_mock):
    # arrange

    # act
    response = await http.request(
        'POST',
        '/public/v2/get-my-offers-mobile/',
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


async def test_v1_get_offers_mobile_public__load_offers_with_degradation_integrations__offers_data(http, pg):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers_offences.sql')
    # act
    response = await http.request(
        'POST',
        '/public/v2/get-my-offers-mobile/',
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
                    'canViewSimilarOffers': False
                },
                'category': 'landSale',
                'cianUserId': 29437831,
                'complaints': None,
                'isDeclined': False,
                'coworkingId': None,
                'deactivatedService': None,
                'dealType': 'sale',
                'description': ANY,
                'formattedAddress': '???????????????????????? ????????, ?????????????????????????? ??????????, ??????. '
                                    '??????????????, ?????????????? ???????? ??????',
                'formattedInfo': '?????????????????? ?????????????? ??? 14.93\xa0??????.',
                'formattedPrice': '2\xa0594\xa0400\xa0???',
                'hasPhotoOffence': False,
                'hasVideoOffence': False,
                'identificationPending': False,
                'isArchived': False,
                'isAuction': False,
                'isObjectOnPremoderation': False,
                'isPrivateAgent': True,
                'offerId': 209194477,
                'cianId': 209194477,
                'offerType': 'suburban',
                'photo': 'https://cdn-p.cian.site/images/1/138/977/779831175-2.jpg',
                'price': {
                    'currency': 'rur',
                    'value': 2594400.0
                },
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
                'status': 'published'
            }
        ],
        'page': {'canLoadMore': False, 'limit': 20, 'offset': 0}}


async def test_v1_get_offers_mobile_public__load_offers_with_pagination__offers_data(
        http,
        pg,
        mobile_offers_integrations_mock,
):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers_for_pagination.sql')
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers_offences.sql')

    # act
    response = await http.request(
        'POST',
        '/public/v2/get-my-offers-mobile/',
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
    assert response.data == {'offers': [
        {
            'archivedDate': None,
            'auction': {
                'concurrencyTypeTitle': 'string',
                'concurrencyTypes': [
                    {'isActive': True,
                     'name': 'string',
                     'type': 'region'
                     }
                ],
                'currentBet': 0.0,
                'increaseBetsPositionsCount': 0,
                'isAvailableAuction': True,
                'isFixedBet': True,
                'isStrategyEnabled': True,
                'noteBet': 'string',
                'strategyDescription': 'string'
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
                'canViewSimilarOffers': False
            },
            'category': 'landSale',
            'cianUserId': 29437831,
            'complaints': None,
            'isDeclined': False,
            'coworkingId': None,
            'deactivatedService': None,
            'dealType': 'sale',
            'description': ANY,
            'formattedAddress': '???????????????????????? ????????, ?????????????????????????? ??????????, ??????. '
                                '??????????????, ?????????????? ???????? ??????',
            'formattedInfo': '?????????????????? ?????????????? ??? 14.93\xa0??????.',
            'formattedPrice': '2\xa0594\xa0400\xa0???',
            'hasPhotoOffence': False,
            'hasVideoOffence': False,
            'identificationPending': False,
            'isArchived': False,
            'isAuction': False,
            'isObjectOnPremoderation': False,
            'isPrivateAgent': True,
            'offerId': 209194477,
            'cianId': 209194477,
            'offerType': 'suburban',
            'photo': 'https://cdn-p.cian.site/images/1/138/977/779831175-2.jpg',
            'price': {'currency': 'rur', 'value': 2594400.0},
            'publishTillDate': None,
            'realtyUserId': 29437831,
            'services': ['paid'],
            'stats': {
                'callsCount': 10,
                'competitorsCount': None,
                'dailyViews': 0,
                'duplicatesCount': None,
                'favorites': None,
                'skippedCallsCount': 9,
                'totalViews': 0,
            },
            'status': 'published'
        }
    ],
        'page': {'canLoadMore': True, 'limit': 1, 'offset': 0}
    }


async def test_v1_get_offers_mobile_public__load_offers_with_enrichment__offers_data(
        http,
        pg,
        moderation_mock,
        callbook_mock,
        monolith_cian_bill_mock,
        mobile_offers_integrations_mock
):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers_for_pagination.sql')
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers_offences.sql')

    await callbook_mock.add_stub(
        method='POST',
        path='/v1/get-user-calls-by-offers-totals/',
        response=MockResponse(
            body={
                'data': [
                    {
                        'callsCount': 10,
                        'missedCallsCount': 9,
                        'offerId': 209194477,
                    }
                ]
            }
        ),
    )
    await moderation_mock.add_stub(
        method='POST',
        path='/v1/get-video-offences-for-announcements/',
        response=MockResponse(
            body={
                'items': [
                    {
                        'announcementId': 209194477,
                        'title': 'string',
                        'comment': 'string',
                        'videoIds': [
                            'string'
                        ]
                    }
                ]
            }
        ),
    )
    await moderation_mock.add_stub(
        method='POST',
        path='/v1/get-image-offences-for-announcements/',
        response=MockResponse(
            body={
                'items': [
                    {
                        'announcementId': 209194477,
                        'title': 'string',
                        'comment': 'string',
                        'imageIds': [
                            0
                        ]
                    }
                ]
            }
        ),
    )
    await monolith_cian_bill_mock.add_stub(
        method='GET',
        path='/v1/tariffication/get-deactivated-additional-services/',
        response=MockResponse(
            body={
                'deactivatedServices': [{
                    'announcementId': 209194477,
                    'serviceType': 'Highlight',
                    'isAutoRestoreOnPaymentEnabled': True,
                    'auctionBet': None
                }, {
                    'announcementId': 209194477,
                    'serviceType': 'auction',
                    'isAutoRestoreOnPaymentEnabled': True,
                    'auctionBet': 10
                }],
                'isAutoRestoreOnPaymentEnabled': True,
            }
        )
    )

    # act
    response = await http.request(
        'POST',
        '/public/v2/get-my-offers-mobile/',
        headers={
            'X-Real-UserId': 29437831
        },
        json={
            'limit': 1,
            'offset': 0,
            'tabType': 'inactive',
        }
    )

    # assert
    assert response.data == {'offers': [
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
                'canViewSimilarOffers': False
            },
            'category': 'landSale',
            'cianUserId': 29437831,
            'complaints': [
                {
                    'comment': '???????????????? ???????????????? ???????????????? ????????????????',
                    'date': '2021-02-04T14:21:28.276339+00:00',
                    'id': 1833685,
                }
            ],
            'isDeclined': False,
            'coworkingId': None,
            'deactivatedService': {
                'description': '?????????????????? ???????????? ?? ???????????? 10 ???/??????. ?????????????????? ????-???? ???????????????? ??????????????. ?????????? ????????????????????'
                               ' ?????????????? ?????????? ?????????? ???????????????????????? ??????????????????????????.',
                'isAutoRestoreOnPaymentEnabled': True
            },
            'dealType': 'sale',
            'description': ANY,
            'formattedAddress': '???????????????????????? ????????, ?????????????????????????? ??????????, ??????. '
                                '??????????????, ?????????????? ???????? ??????',
            'formattedInfo': '?????????????????? ?????????????? ??? 14.93\xa0??????.',
            'formattedPrice': '2\xa0594\xa0400\xa0???',
            'hasPhotoOffence': True,
            'hasVideoOffence': True,
            'identificationPending': False,
            'isArchived': False,
            'isAuction': False,
            'isObjectOnPremoderation': False,
            'isPrivateAgent': True,
            'offerId': 209194477,
            'cianId': 209194477,
            'offerType': 'suburban',
            'photo': 'https://cdn-p.cian.site/images/1/138/977/779831175-2.jpg',
            'price': {'currency': 'rur', 'value': 2594400.0},
            'publishTillDate': None,
            'realtyUserId': 29437831,
            'services': ['paid'],
            'stats': {
                'callsCount': None,
                'competitorsCount': None,
                'dailyViews': None,
                'duplicatesCount': None,
                'favorites': None,
                'skippedCallsCount': None,
                'totalViews': None
            },
            'status': 'published'
        }
    ],
        'page': {'canLoadMore': False, 'limit': 1, 'offset': 0}
    }


async def test_v1_get_offers_mobile_public__load_rent_offers__offers_data(http, pg, mobile_offers_integrations_mock):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'agents_hiearachy.sql')
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers_offences.sql')
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers_premoderations.sql')

    # act
    response = await http.request(
        'POST',
        '/public/v2/get-my-offers-mobile/',
        headers={
            'X-Real-UserId': 29437831
        },
        json={
            'limit': 20,
            'offset': 0,
            'tabType': 'rent'
        }
    )

    assert response.data == {'offers': [], 'page': {'canLoadMore': False, 'limit': 20, 'offset': 0}}


async def test_v2_get_offers_mobile_public__get_archived_removed_by_moderator__can_delete_offer(http, pg):
    # arrange
    expected = {
        'canChangePublisher': False,
        'canDelete': True,
        'canEdit': False,
        'canMoveToArchive': False,
        'canRaise': False,
        'canRaiseWithoutAddform': False,
        'canRestore': False,
        'canUpdateEditDate': False,
        'canViewSimilarOffers': False
    }
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers_for_available_actions.sql')

    # act
    response = await http.request(
        'POST',
        '/public/v2/get-my-offers-mobile/',
        headers={
            'X-Real-UserId': 27864412
        },
        json={
            'limit': 20,
            'offset': 0,
            'tabType': 'archived',
        }
    )
    assert response.data['offers'][0]['availableActions'] == expected


async def test_v2_get_offers_mobile_public__get_declined_removed_by_moderator__cant_delete_offer(http, pg):
    # arrange
    expected = {
        'canChangePublisher': False,
        'canDelete': False,
        'canEdit': False,
        'canMoveToArchive': False,
        'canRaise': False,
        'canRaiseWithoutAddform': False,
        'canRestore': False,
        'canUpdateEditDate': False,
        'canViewSimilarOffers': False
    }
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers_for_available_actions.sql')

    # act
    response = await http.request(
        'POST',
        '/public/v2/get-my-offers-mobile/',
        headers={
            'X-Real-UserId': 27864413
        },
        json={
            'limit': 20,
            'offset': 0,
            'tabType': 'declined',
        }
    )
    assert response.data['offers'][0]['availableActions'] == expected
