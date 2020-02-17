import pytest
from cian_test_utils import future

from my_offers import pg
from my_offers.repositories.postgresql import get_object_models
from tests.utils import load_data


@pytest.mark.gen_test
async def test_get_object_models__empty_filter__result(mocker):
    # arrange
    filters = {}

    pg.get().fetch.return_value = future([])
    query = load_data(__file__, 'get_object_models_empty_filter.sql').strip()
    expected = []

    # act
    result = await get_object_models(filters=filters)

    # assert
    assert result == expected

    pg.get().fetch.assert_called_once_with(query, 20)


@pytest.mark.gen_test
async def test_get_object_models__full_filter__result(mocker):
    # arrange
    filters = {
        'status_tab': 'active',
        'deal_type': 'sale',
        'offer_type': 'suburban',
        'services': ['paid'],
        'sub_agent_ids': [46610424],
        'has_photo': True,
        'is_manual': False,
        'is_in_hidden_base': False,
        'search_text': '+79112318015',
        'master_user_id': 12478339,
    }

    pg.get().fetch.return_value = future([])
    query = load_data(__file__, 'get_object_models_full_filter.sql').strip()

    expected = []

    # act
    result = await get_object_models(filters=filters, limit=40)

    # assert
    assert result == expected

    pg.get().fetch.assert_called_once_with(
        query,
        'sale',
        12478339,
        'suburban',
        [46610424],
        40,
        ['paid'],
        'active',
        'russian',
        '+79112318015',
    )


@pytest.mark.gen_test
async def test_get_object_models__full_filter_none__result(mocker):
    # arrange
    filters = {
        'status_tab': 'active',
        'deal_type': 'sale',
        'offer_type': None,
        'services': ['paid'],
        'sub_agent_ids': [46610424],
        'has_photo': True,
        'is_manual': False,
        'is_in_hidden_base': False,
        'search_text': '+79112318015',
        'master_user_id': 12478339,
    }

    pg.get().fetch.return_value = future([])
    query = load_data(__file__, 'get_object_models_full_filter_none.sql').strip()

    expected = []

    # act
    result = await get_object_models(filters=filters, limit=40)

    # assert
    assert result == expected

    pg.get().fetch.assert_called_once_with(
        query,
        'sale',
        12478339,
        [46610424],
        40,
        ['paid'],
        'active',
        'russian',
        '+79112318015',
    )
