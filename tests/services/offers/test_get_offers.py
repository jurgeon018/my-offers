import pytest
from cian_test_utils import future

from my_offers.entities.get_offers import Filter
from my_offers.enums import OfferStatusTab
from my_offers.services.offers._filters import get_counter_filters
from my_offers.services.offers import get_filters

PATH = 'my_offers.services.offers._get_offers.'


@pytest.mark.gen_test
async def test_get_filters(mocker):
    # arrange
    filters = Filter(
        status_tab=OfferStatusTab.active,
        is_manual=True,
        deal_type=None,
        offer_type=None,
        services=None,
        sub_agent_ids=None,
        has_photo=None,
        is_in_hidden_base=None,
        search_text=None,
    )

    get_master_user_id_mock = mocker.patch(
        'my_offers.services.offers._filters.get_master_user_id',
        return_value=future()
    )
    expected = {'is_manual': True, 'master_user_id': 77, 'status_tab': 'active'}

    # act
    result = await get_filters(filters=filters, user_id=77)

    # assert
    assert result == expected
    get_master_user_id_mock.assert_called_once_with(77)


@pytest.mark.gen_test
async def test_get_filters__all__for_all(mocker):
    # arrange
    filters = Filter(
        status_tab=OfferStatusTab.all,
        is_manual=True,
        deal_type=None,
        offer_type=None,
        services=None,
        sub_agent_ids=None,
        has_photo=None,
        is_in_hidden_base=None,
        search_text=None,
    )

    get_master_user_id_mock = mocker.patch(
        'my_offers.services.offers._filters.get_master_user_id',
        return_value=future()
    )
    expected = {'is_manual': True, 'master_user_id': 77}

    # act
    result = await get_filters(filters=filters, user_id=77)

    # assert
    assert result == expected
    get_master_user_id_mock.assert_called_once_with(77)


def test_get_counter_filters__search_text__search_text():
    # arrange
    filters = {
        'master_user_id': 77,
        'search_text': 'zzz'
    }

    expected = {
        'master_user_id': 77,
        'user_id': None,
        'search_text': 'zzz',
    }

    # act
    result = get_counter_filters(filters)

    # assert
    assert result == expected


@pytest.mark.gen_test
async def test_get_filters__sub_agent__filters(mocker):
    # arrange
    filters = Filter(
        status_tab=OfferStatusTab.active,
        is_manual=True,
        deal_type=None,
        offer_type=None,
        services=None,
        sub_agent_ids=None,
        has_photo=None,
        is_in_hidden_base=None,
        search_text=None,
    )

    get_master_user_id_mock = mocker.patch(
        'my_offers.services.offers._filters.get_master_user_id',
        return_value=future(88)
    )
    expected = {'is_manual': True, 'master_user_id': [88, 77], 'status_tab': 'active', 'user_id': 77}

    # act
    result = await get_filters(filters=filters, user_id=77)

    # assert
    assert result == expected
    get_master_user_id_mock.assert_called_once_with(77)


@pytest.mark.gen_test
async def test_get_filters__search_text__filters(mocker):
    # arrange
    filters = Filter(
        status_tab=OfferStatusTab.active,
        is_manual=True,
        deal_type=None,
        offer_type=None,
        services=None,
        sub_agent_ids=None,
        has_photo=None,
        is_in_hidden_base=None,
        search_text='+7 929 333 55 57 Москва',
    )

    get_master_user_id_mock = mocker.patch(
        'my_offers.services.offers._filters.get_master_user_id',
        return_value=future(88)
    )
    expected = {
        'is_manual': True,
        'master_user_id': [88, 77],
        'status_tab': 'active',
        'user_id': 77,
        'search_text': ' 9293335557 Москва',
    }

    # act
    result = await get_filters(filters=filters, user_id=77)

    # assert
    assert result == expected
    get_master_user_id_mock.assert_called_once_with(77)
