import pytest
from cian_test_utils import future

from my_offers import pg
from my_offers.enums import GetOffersSortType
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
        'my_offers.repositories.postgresql.object_model.object_model_mapper.map_from',
        return_value=object_model,
    )
    expected = ([object_model], 1)

    # act
    result = await get_object_models(filters=filters, limit=20, offset=0, sort_type=GetOffersSortType.by_default)

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

    expected = ([], 0)

    # act
    result = await get_object_models(filters=filters, limit=40, offset=0, sort_type=GetOffersSortType.by_default)

    # assert
    assert result == expected

    pg.get().fetch.assert_called_once_with(
        'SELECT offers.raw_data, count(*) OVER () AS total_count \nFROM offers \nWHERE offers.status_tab = $8 '
        'AND offers.deal_type = $1 AND offers.offer_type = $3 AND offers.user_id = ANY (CAST($4 AS BIGINT[])) '
        'AND offers.has_photo = true AND offers.is_manual = false AND offers.is_in_hidden_base = false '
        'AND offers.master_user_id = $2 AND offers.services && $7 '
        'AND to_tsvector($9, offers.search_text) @@ to_tsquery(\'russian\', $10) '
        'ORDER BY offers.sort_date DESC NULLS LAST, offers.offer_id \n LIMIT $5 OFFSET $6',
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
async def test_get_object_models__filter_none__result(mocker):
    # arrange
    filters = {
        'offer_type': None,
    }

    pg.get().fetch.return_value = future([])

    expected = ([], 0)

    # act
    result = await get_object_models(filters=filters, limit=40, offset=0, sort_type=GetOffersSortType.by_default)

    # assert
    assert result == expected

    pg.get().fetch.assert_called_once_with(
        'SELECT offers.raw_data, count(*) OVER () AS total_count \nFROM offers '
        'ORDER BY offers.sort_date DESC NULLS LAST, offers.offer_id \n LIMIT $1 OFFSET $2',
        40,
        0,
    )


@pytest.mark.gen_test
async def test_get_object_models___wrong_filter__result(mocker):
    # arrange
    filters = {
        'zzzz': 'AAAA',
        'yyyy': None,
    }

    pg.get().fetch.return_value = future([])

    expected = ([], 0)

    # act
    result = await get_object_models(filters=filters, limit=40, offset=0, sort_type=GetOffersSortType.by_default)

    # assert
    assert result == expected

    pg.get().fetch.assert_called_once_with(
        'SELECT offers.raw_data, count(*) OVER () AS total_count \nFROM offers '
        'ORDER BY offers.sort_date DESC NULLS LAST, offers.offer_id \n LIMIT $1 OFFSET $2',
        40,
        0
    )
