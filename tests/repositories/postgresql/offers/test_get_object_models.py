import pytest
from cian_test_utils import future

from my_offers import pg
from my_offers.repositories.postgresql import get_object_models
from tests.utils import load_data


@pytest.mark.gen_test
async def test_get_object_models__empty_filter__result(mocker):
    # arrange
    filters = {}
    object_model = mocker.sentinel.object_model

    pg.get().fetch.return_value = future([{'raw_data': '{"id": 12}', 'total_count': 1}])
    query = load_data(__file__, 'get_object_models_empty_filter.sql').strip()
    mocker.patch(
        'my_offers.repositories.postgresql.object_models.object_model_mapper.map_from',
        return_value=object_model,
    )
    expected = ([object_model], 1)

    # act
    result = await get_object_models(filters=filters, limit=20, offset=0)

    # assert
    assert result == expected

    pg.get().fetch.assert_called_once_with(query, 20, 0)


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

    expected = ([], 0)

    # act
    result = await get_object_models(filters=filters, limit=40, offset=0)

    # assert
    assert result == expected

    pg.get().fetch.assert_called_once_with(
        query,
        'sale',
        12478339,
        'suburban',
        [46610424],
        40,
        0,
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

    expected = ([], 0)

    # act
    result = await get_object_models(filters=filters, limit=40, offset=0)

    # assert
    assert result == expected

    pg.get().fetch.assert_called_once_with(
        query,
        'sale',
        12478339,
        [46610424],
        40,
        0,
        ['paid'],
        'active',
        'russian',
        '+79112318015',
    )
