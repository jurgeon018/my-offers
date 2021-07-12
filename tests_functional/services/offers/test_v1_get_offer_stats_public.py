import asyncio
from pathlib import Path

import pytest
from cian_functional_test_utils.data_fixtures import load_json_data
from cian_functional_test_utils.pytest_plugin import MockResponse


@pytest.fixture(autouse=True)
async def _setup(pg):
    await pg.execute_scripts(Path(__file__).parent / 'data' / 'test_v1_get_offer_stats_public_setup.sql')


async def test_normal_flow__return_expected(http, monolith_python_mock, callbook_mock, favorites_mock):
    # arrange
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
        favorites_mock.add_stub(
            method='POST',
            path='/v1/get-offers-favorites-count/',
            response=MockResponse(
                body=[
                    {
                        'count': 13,
                        'offerId': 209194477,
                    },
                ],
            ),
        ),
        monolith_python_mock.add_stub(
            method='GET',
            path='/cian-api/site/v1/get-my-offer-stats/',
            response=MockResponse(
                body=load_json_data(__file__, 'cian_api_site_v1_get_my_offer_stats_response.json'),
            ),
        ),
    )

    # act
    response = await http.request(
        'GET',
        '/public/v1/get-offer-stats/',
        params={
            'offerId': 209194477,
        },
        headers={
            'X-Real-UserId': 15327749
        },
    )

    # assert
    assert response.data == {
        'data': {
            'day10': {
                'callsTotal': 10,
                'coverage': 31.0,
                'favoritesTotal': 13,
                'offerShow': 58,
                'offerShowTotal': 431,
                'phoneShow': 2,
                'searchResultsShow': 108,
                'searchResultsSelectedChart': [
                    {'date': '2021-06-22', 'value': 15},
                    {'date': '2021-06-23', 'value': 53},
                    {'date': '2021-06-24', 'value': 26},
                ],
                'searchResultsShowChart': [
                    {'date': '2021-06-22', 'value': 3},
                    {'date': '2021-06-23', 'value': 10},
                    {'date': '2021-06-24', 'value': 1},
                ],
                'showChart': [
                    {'date': '2021-06-22', 'value': 3},
                    {'date': '2021-06-23', 'value': 4},
                    {'date': '2021-06-24', 'value': 1},
                ]
            },
            'month': {
                'callsTotal': 10,
                'coverage': 27.0,
                'favoritesTotal': 13,
                'offerShow': 91,
                'offerShowTotal': 431,
                'phoneShow': 2,
                'searchResultsShow': 148,
                'searchResultsSelectedChart': [
                    {'date': '2021-06-30', 'value': 33},
                    {'date': '2021-07-01', 'value': 19},
                    {'date': '2021-07-02', 'value': 15},
                ],
                'searchResultsShowChart': [
                    {'date': '2021-06-30', 'value': 20},
                    {'date': '2021-07-01', 'value': 11},
                    {'date': '2021-07-02', 'value': 5},
                ],
                'showChart': [
                    {'date': '2021-06-30', 'value': 6},
                    {'date': '2021-07-01', 'value': 6},
                    {'date': '2021-07-02', 'value': 3},
                ],
            },
        },
        'emergencyMessage': None,
    }


async def test_no_data_available__return_default(http, monolith_python_mock, callbook_mock, favorites_mock):
    # arrange
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
        favorites_mock.add_stub(
            method='POST',
            path='/v1/get-offers-favorites-count/',
            response=MockResponse(
                body=[
                    {
                        'count': 13,
                        'offerId': 209194477,
                    },
                ],
            ),
        ),
        monolith_python_mock.add_stub(
            method='GET',
            path='/cian-api/site/v1/get-my-offer-stats/',
            response=MockResponse(
                body=load_json_data(__file__, 'cian_api_site_v1_get_my_offer_stats__no_data_response.json'),
            ),
        ),
    )

    # act
    response = await http.request(
        'GET',
        '/public/v1/get-offer-stats/',
        params={
            'offerId': 209194477,
            'offerType': 'flat',
            'dealType': 'rent',
        },
        headers={
            'X-Real-UserId': 15327749
        },
    )

    # assert
    assert response.data == {
        'data': {
            'day10': {
                'callsTotal': 10,
                'coverage': None,
                'favoritesTotal': 13,
                'offerShow': None,
                'offerShowTotal': None,
                'phoneShow': None,
                'searchResultsShow': None,
                'searchResultsSelectedChart': None,
                'searchResultsShowChart': None,
                'showChart': None,
            },
            'month': {
                'callsTotal': 10,
                'coverage': 27.0,
                'favoritesTotal': 13,
                'offerShow': 91,
                'offerShowTotal': 431,
                'phoneShow': 2,
                'searchResultsShow': 148,
                'searchResultsSelectedChart': [
                    {'date': '2021-06-30', 'value': 33},
                    {'date': '2021-07-01', 'value': 19},
                    {'date': '2021-07-02', 'value': 15},
                ],
                'searchResultsShowChart': [
                    {'date': '2021-06-30', 'value': 20},
                    {'date': '2021-07-01', 'value': 11},
                    {'date': '2021-07-02', 'value': 5},
                ],
                'showChart': [
                    {'date': '2021-06-30', 'value': 6},
                    {'date': '2021-07-01', 'value': 6},
                    {'date': '2021-07-02', 'value': 3},
                ],
            },
        },
        'emergencyMessage': None,
    }
