import pytest
from cian_test_utils import future

from my_offers.repositories.geo_subdomain.entities import GetSubdomainsResponse
from my_offers.services.geo_subdomains.get_subdomain_by_location_id import (
    get_subdomain_data_by_location_ids,
    get_subdomain_map,
)


pytestmark = pytest.mark.gen_test


async def test_get_subdomain_map(mocker):
    # arrange
    mocker.patch(
        'my_offers.services.geo_subdomains.get_subdomain_by_location_id.get_operation_id',
        return_value=1,
    )
    mocker.patch(
        'my_offers.services.geo_subdomains.get_subdomain_by_location_id.new_operation_id',
    )

    v1_get_subdomains_mock = mocker.patch(
        'my_offers.services.geo_subdomains.get_subdomain_by_location_id.v1_get_subdomains',
        return_value=future(
            GetSubdomainsResponse(
                subdomains=[
                    {
                        'locations': [
                            {
                                'location_id': 1
                            }
                        ]
                    }
                ]
            )
        )
    )

    # act
    result = await get_subdomain_map()

    # assert
    assert result == {
        '1': {
            'locations': [
                {
                    'location_id': 1
                }
            ]
        }
    }
    v1_get_subdomains_mock.assert_called_once()


def test_get_subdomain_data_by_location_ids__not_found_subdomain__return_default():
    # arrange
    geo_subdomain_map = {
        '2': {
            'locations': [
                {
                    'location_id': 2
                }
            ]
        },
        '1': {
            'locations': [
                {
                    'location_id': 1
                }
            ]
        }
    }
    location_ids = [100, 200, 300]

    # act
    result = get_subdomain_data_by_location_ids(
        location_ids=location_ids,
        geo_subdomain_map=geo_subdomain_map,
    )

    # assert
    assert result == {
        'locations': [
            {
                'location_id': 1
            }
        ]
    }


def test_get_subdomain_data_by_location_ids():
    # arrange
    geo_subdomain_map = {
        '2': {
            'locations': [
                {
                    'location_id': 2
                }
            ]
        },
        '1': {
            'locations': [
                {
                    'location_id': 1
                }
            ]
        }
    }
    location_ids = [2]

    # act
    result = get_subdomain_data_by_location_ids(
        location_ids=location_ids,
        geo_subdomain_map=geo_subdomain_map,
    )

    # assert
    assert result == {
        'locations': [
            {
                'location_id': 2
            }
        ]
    }
