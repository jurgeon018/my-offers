from datetime import datetime

import freezegun
import pytest
import pytz
from freezegun.api import FakeDatetime

from my_offers import enums, pg
from my_offers.entities import Offer
from my_offers.enums import OfferServices
from my_offers.repositories.postgresql import save_offer


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
        services=[OfferServices.auction],
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
        'INSERT INTO offers (offer_id, master_user_id, user_id, deal_type, offer_type, status_tab, services, '
        'search_text, is_manual, is_in_hidden_base, has_photo, row_version, raw_data, created_at, updated_at, '
        'total_area, price, price_per_meter, walking_time, street_name, sort_date, is_test) '
        'VALUES ($8, $7, $22, $2, $9, $18, $16, $15, $5, $4, $3, $14, $12, $1, $21, $20, $10, $11, $23, $19, $17, $6) '
        'ON CONFLICT (offer_id) DO UPDATE SET master_user_id = excluded.master_user_id, user_id = excluded.user_id, '
        'deal_type = excluded.deal_type, offer_type = excluded.offer_type, status_tab = excluded.status_tab, '
        'services = excluded.services, search_text = excluded.search_text, is_manual = excluded.is_manual, '
        'is_in_hidden_base = excluded.is_in_hidden_base, has_photo = excluded.has_photo, '
        'row_version = excluded.row_version, raw_data = excluded.raw_data, updated_at = excluded.updated_at, '
        'total_area = excluded.total_area, price = excluded.price, price_per_meter = excluded.price_per_meter, '
        'walking_time = excluded.walking_time, street_name = excluded.street_name, sort_date = excluded.sort_date, '
        'is_test = excluded.is_test WHERE offers.row_version < $13',
        FakeDatetime(2020, 2, 10, 9, 57, 30, 303690, tzinfo=pytz.UTC),
        'rent',
        False,
        False,
        True,
        False,
        2222,
        1111,
        'flat',
        100000.0,
        2000.0,
        '{"offer_id": 1111}',
        4444444,
        4444444,
        'zzzzzzz',
        ['auction'],
        FakeDatetime(2020, 2, 7, 0, 0),
        'active',
        'AAAAA',
        5000.0,
        FakeDatetime(2020, 2, 10, 9, 57, 30, 303690, tzinfo=pytz.UTC),
        3333,
        15.0
    )
