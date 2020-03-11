import pytest
from cian_settings.entities import Filter
from cian_test_utils import future

from my_offers.entities import GetOffersPrivateRequest
from my_offers.enums import GetOfferStatusTab
from my_offers.services.offers import v2_get_offers_private


@pytest.mark.gen_test
async def test_get_offers_private(mocker):
    # arrange
    request = GetOffersPrivateRequest(
        user_id=111,
        filters=Filter(
            status_tab=GetOfferStatusTab.active,
            sort_type=None,
            deal_type=None,
            offer_type=None,
            services=None,
            sub_agent_ids=None,
            has_photo=None,
            is_manual=None,
            is_in_hidden_base=None,
            search_text=None,
        ),
        pagination=None,
        sort=None,
    )

    response = mocker.sentinel.response

    get_offers_public_mock = mocker.patch(
        'my_offers.services.offers._get_offers.get_offers_public',
        return_value=future(response),
    )

    # act
    result = await v2_get_offers_private(request)

    # assert
    assert result == response
    get_offers_public_mock.assert_called_once_with(
        request=request,
        realty_user_id=111,
    )