import pytest
from cian_test_utils import future

from my_offers.repositories.monolith_cian_realty.entities import GetRegionsResponse
from my_offers.services.get_region_ids import get_region_ids_cached


@pytest.mark.gen_test
async def test_get_region_ids_cached(mocker):
    # arrange
    subdomain1 = {
        'locations': [{'location_id': 100}]
    }
    subdomain2 = {
        'locations': [{'location_id': 200}]
    }
    subdomain3 = {
        'locations': [{'location_id': 300}]
    }
    get_subdomain_map_mock = mocker.patch(
        'my_offers.services.get_region_ids.get_subdomain_map',
        return_value=future(
            {
                '100': subdomain1,
                '200': subdomain2,
                '300': subdomain3,
            }
        )
    )
    api_geo_get_regions_mock = mocker.patch(
        'my_offers.services.get_region_ids.api_geo_get_regions',
        return_value=future([
            GetRegionsResponse(id=10),
            GetRegionsResponse(id=20),
            GetRegionsResponse(id=30),
        ])
    )

    # act
    region_ids = await get_region_ids_cached()

    # assert
    assert region_ids == {-1, -2, 10, 20, 30, 100, 200, 300}
    get_subdomain_map_mock.assert_called_once_with()
    api_geo_get_regions_mock.assert_called_once_with()
