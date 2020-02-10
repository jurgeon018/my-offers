from datetime import datetime

import pytest

from my_offers import enums, pg
from my_offers.entities import Offer
from my_offers.repositories.postgresql import save_offer


@pytest.mark.gen_test
async def test_save_offer():
    # arrange
    offer = Offer(
        offer_id=1111,
        master_user_id=2222,
        user_id=3333,
        deal_type=enums.DealType.rent,
        offer_type=enums.OfferType.flat,
        status_tab=enums.OfferStatusTab.active,
        search_text='zzzzzzz',
        row_version=4444444,
        raw_data={'offer_id': 1111},
        services=[enums.Services.auction],
        is_manual=True,
        is_in_hidden_base=False,
        has_photo=False,
        is_test=False,
        price=100000,
        price_per_meter=2000,
        total_area=5000,
        walking_time=15,
        street_name='AAAAA',
        sort_date=datetime(2020, 2, 7),
    )

    # act
    await save_offer(offer)

    # assert
    pg.get().execute.assert_called_once()
