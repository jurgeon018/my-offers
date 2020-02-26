import pytest
from cian_test_utils import future

from my_offers.repositories.newbuilding_search.entities import (
    GetNewbuildingByIdsItem,
    GetNewBuildingsByIdsRequest,
    GetNewBuildingsByIdsResponse,
)
from my_offers.services.newbuilding.newbuilding_url import get_newbuilding_urls


PATH = 'my_offers.services.newbuilding.newbuilding_url.'


@pytest.mark.gen_test
async def test_get_newbuilding_url_cached(mocker):
    # arrange
    expected = {11: 'zzzz'}
    v1_get_newbuildings_by_ids_mock = mocker.patch(
        f'{PATH}v1_get_newbuildings_by_ids',
        return_value=future(GetNewBuildingsByIdsResponse(items=[GetNewbuildingByIdsItem(id=11, url='zzzz')]))
    )

    # act
    result = await get_newbuilding_urls(jk_ids=[11])

    # assert
    assert result == expected

    v1_get_newbuildings_by_ids_mock.assert_called_once_with(GetNewBuildingsByIdsRequest(ids=[11]))


@pytest.mark.gen_test
async def test_get_newbuilding_url_cached__not_found__none(mocker):
    # arrange
    v1_get_newbuildings_by_ids_mock = mocker.patch(
        f'{PATH}v1_get_newbuildings_by_ids',
        return_value=future(GetNewBuildingsByIdsResponse(items=[]))
    )

    # act
    result = await get_newbuilding_urls(jk_ids=[11])

    # assert
    assert result == {}

    v1_get_newbuildings_by_ids_mock.assert_called_once_with(GetNewBuildingsByIdsRequest(ids=[11]))
