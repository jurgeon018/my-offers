import pytest
from cian_test_utils import future

from my_offers.entities.get_offers import Filter
from my_offers.enums import OfferStatusTab
from my_offers.services.offers._get_offers import get_filters


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
        f'{PATH}get_master_user_id',
        return_value=future()
    )
    expected = {'is_manual': True, 'master_user_id': 77, 'status_tab': 'active'}

    # act
    result = await get_filters(filters=filters, user_id=77)

    # assert
    assert result == expected
    get_master_user_id_mock.assert_called_once_with(77)


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
        f'{PATH}get_master_user_id',
        return_value=future(88)
    )
    expected = {'is_manual': True, 'master_user_id': [88, 77], 'status_tab': 'active', 'user_id': 77}

    # act
    result = await get_filters(filters=filters, user_id=77)

    # assert
    assert result == expected
    get_master_user_id_mock.assert_called_once_with(77)
