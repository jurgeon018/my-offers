import time
from typing import TYPE_CHECKING

import pytest
from requests import HTTPError

from tests_api.helper import MyOffersHelper
from .cian.my_offers.entities import OfferActionRequest
from .cian.my_offers.entities.offer_action_response import Status


if TYPE_CHECKING:
    from .cian.services import CianServices


class TestPublicV1GetOffers(MyOffersHelper):
    @pytest.mark.base
    @pytest.mark.skip
    def test_200_post(self, sl: 'CianServices', context):
        # todo: https://jira.cian.tech/browse/CD-75751
        # arrange
        user = self.create_user(sl, 'base', True, 1)
        offer = self.create_offer(sl, user_id=user.userId)

        # ждем появления оффера в my-offers
        time.sleep(10)

        # act
        with context.x_real_user(user_id=user.userId):
            response = sl.my_offers.public_v1_actions_update_edit_date.request_post(
                data=OfferActionRequest(offerId=offer.realtyObjectId)
            )

        # assert
        assert response.status == Status.ok

    @pytest.mark.base
    def test_400_post(self, sl: 'CianServices', context):
        # arrange
        user = self.create_user(sl, 'base', True, 1)
        offer = self.create_offer(sl, user_id=user.userId)

        # ждем появления оффера в my-offers
        time.sleep(10)

        # act
        with pytest.raises(HTTPError) as error, context.x_real_user(user_id=1):
            sl.my_offers.public_v1_actions_update_edit_date.request_post(
                data=OfferActionRequest(offerId=offer.realtyObjectId)
            )

        # assert
        assert error.value.response.status_code == 400
