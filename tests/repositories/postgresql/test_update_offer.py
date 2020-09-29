from datetime import datetime

import pytest
import pytz
from freezegun import freeze_time
from freezegun.api import FakeDatetime

from my_offers import entities, enums, pg
from my_offers.repositories.postgresql.offer import update_offer, update_offer_master_user_id_and_payed_by


@pytest.mark.gen_test
@freeze_time('2020-03-12')
async def test_update_offer():
    # arrange
    offer = entities.Offer(
        offer_id=1111,
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
        payed_by=None,
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
        'UPDATE offers SET offer_id=$7, master_user_id=$6, user_id=$22, deal_type=$1, offer_type=$9, status_tab=$18, '
        'services=CAST($16 AS offer_service[]), search_text=$15, is_manual=$4, is_in_hidden_base=$3, has_photo=$2, '
        'row_version=$13, raw_data=$12, updated_at=$21, total_area=$20, price=$10, price_per_meter=$11, '
        'walking_time=$23, street_name=$19, sort_date=$17, is_test=$5 '
        'WHERE offers.offer_id = $8 AND offers.row_version <= $14',
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
        '{"offer_id": 1111}', 4444444,
        4444444, 'zzzzzzz', ['auction'],
        FakeDatetime(2020, 2, 7, 0, 0),
        'active',
        'AAAAA',
        5000.0,
        FakeDatetime(2020, 3, 12, 0, 0, tzinfo=pytz.UTC),
        3333,
        15.0
    )


@pytest.mark.gen_test
@freeze_time('2020-03-12')
async def test_update_offer__min_rowversion__update():
    # arrange
    offer = entities.Offer(
        offer_id=1111,
        master_user_id=2222,
        user_id=3333,
        deal_type=enums.DealType.rent,
        offer_type=enums.OfferType.flat,
        status_tab=enums.OfferStatusTab.active,
        search_text='zzzzzzz',
        row_version=1,
        raw_data={'offer_id': 1111},
        services=[enums.OfferServices.auction],
        is_manual=True,
        is_in_hidden_base=False,
        has_photo=False,
        payed_by=None,
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
        'UPDATE offers SET offer_id=$7, master_user_id=$6, user_id=$20, deal_type=$1, offer_type=$9, status_tab=$16, '
        'services=CAST($14 AS offer_service[]), search_text=$13, is_manual=$4, is_in_hidden_base=$3, has_photo=$2, '
        'raw_data=$12, updated_at=$19, total_area=$18, price=$10, price_per_meter=$11, walking_time=$21, '
        'street_name=$17, sort_date=$15, is_test=$5 WHERE offers.offer_id = $8',
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
        'zzzzzzz',
        ['auction'],
        FakeDatetime(2020, 2, 7, 0, 0),
        'active',
        'AAAAA',
        5000.0,
        FakeDatetime(2020, 3, 12, 0, 0, tzinfo=pytz.UTC),
        3333,
        15.0,
    )


async def test_update_offer_master_user_id():
    # arrange & act
    await update_offer_master_user_id_and_payed_by(offer_id=1, master_user_id=2, payed_by=3)

    # assert
    pg.get().execute.assert_called_once_with(
        '\n    update\n        offers\n    set\n        master_user_id = $1,\n        '
        'payed_by = COALESCE(payed_by, $4)\n    where\n        offer_id = $2\n        and '
        'master_user_id <> $3\n    ',
        2,
        1,
        2,
        3
    )
