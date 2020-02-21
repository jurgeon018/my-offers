from datetime import datetime

import freezegun
import pytest
import pytz

from my_offers import enums, pg
from my_offers.entities import Offer
from my_offers.repositories.monolith_cian_announcementapi.entities.publish_term import Services
from my_offers.repositories.postgresql import save_offer
from tests.utils import load_data


@pytest.mark.gen_test
@freezegun.freeze_time('2020-02-10 09:57:30.303690+00:00')
async def test_save_offer(mocker):
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
        services=[Services.auction],
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
    pg.get().execute.assert_called_once_with(
        load_data(__file__, 'upsert.sql'),
        datetime(2020, 2, 10, 9, 57, 30, 303690, tzinfo=pytz.UTC),
        'rent',
        False,
        False,
        True,
        False,
        2222,
        1111,
        'flat',
        2222,
        False,
        4444444,
        '{"offer_id": 1111}',
        datetime(2020, 2, 10, 9, 57, 30, 303690, tzinfo=pytz.UTC),
        5000.0,
        100000.0,
        2000.0,
        15.0,
        'AAAAA',
        datetime(2020, 2, 7, 0, 0),
        3333,
        False,
        'rent',
        'flat',
        'active',
        ['auction'],
        'zzzzzzz',
        True,
        False,
        100000.0,
        2000.0,
        '{"offer_id": 1111}',
        4444444,
        4444444,
        'zzzzzzz',
        ['auction'],
        datetime(2020, 2, 7, 0, 0),
        'active',
        'AAAAA',
        5000.0,
        datetime(2020, 2, 10, 9, 57, 30, 303690, tzinfo=pytz.UTC),
        3333,
        15.0,
    )
