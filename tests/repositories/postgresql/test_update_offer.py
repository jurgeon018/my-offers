from datetime import datetime

import pytest
import pytz
from freezegun import freeze_time
from freezegun.api import FakeDatetime

from my_offers import entities, enums, pg
from my_offers.repositories.postgresql.offer import update_offer, update_offer_master_user_id


@pytest.mark.gen_test
@freeze_time('2020-03-12')
async def test_update_offer():
    # arrange
    offer = entities.Offer(
        offer_id=1111,
        cian_offer_id=1111,
        master_user_id=2222,
        user_id=3333,
        deal_type=enums.DealType.rent,
        offer_type=enums.OfferType.flat,
        status_tab=enums.OfferStatusTab.active,
        search_text='zzzzzzz',
        row_version=4444444,
        raw_data={'offer_id': 1111},
        services=[enums.OfferServices.auction],
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
    await update_offer(offer)

    # assert
    pg.get().execute.assert_called_once_with(
        'UPDATE offers SET offer_id=$8, cian_offer_id=$1, master_user_id=$7, user_id=$23, deal_type=$2, '
        'offer_type=$10, status_tab=$19, services=CAST($17 AS offer_service[]), search_text=$16, is_manual=$5, '
        'is_in_hidden_base=$4, has_photo=$3, row_version=$14, raw_data=$13, updated_at=$22, total_area=$21, price=$11, '
        'price_per_meter=$12, walking_time=$24, street_name=$20, sort_date=$18, is_test=$6 '
        'WHERE offers.offer_id = $9 '
        'AND offers.row_version <= $15',
        1111,
        'rent',
        False,
        False,
        True,
        False,
        2222,
        1111,
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
        FakeDatetime(2020, 3, 12, 0, 0, tzinfo=pytz.UTC),
        3333,
        15.0
    )


async def test_update_offer_master_user_id():
    # arrange & act
    await update_offer_master_user_id(offer_id=1, master_user_id=2)

    # assert
    pg.get().execute.assert_called_once_with(
        '\n    update offers set master_user_id = $1 where offer_id = $2 and master_user_id <> $3\n    ',
        2,
        1,
        2,
    )
