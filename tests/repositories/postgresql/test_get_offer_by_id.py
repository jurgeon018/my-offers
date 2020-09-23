from datetime import datetime

import pytest
import pytz
from cian_test_utils import future

from my_offers import enums, pg
from my_offers.entities import Offer
from my_offers.repositories.postgresql.offer import get_offer_by_id, get_offers_id_older_than


@pytest.mark.gen_test
@pytest.mark.parametrize(
    ('row', 'expected'),
    (
        (None, None),
        (
            {'id': 1, 'raw_data': '{"zz": "yy"}'},
            Offer(
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
        )
    )
)
async def test_get_offer_by_id(mocker, row, expected):
    # arrange
    mocker.patch('my_offers.repositories.postgresql.offer.offer_mapper.map_from', return_value=expected)
    pg.get().fetchrow.return_value = future(row)

    # act
    result = await get_offer_by_id(111)

    # assert
    assert result == expected


@pytest.mark.gen_test
async def test_get_offers_id_older_than(mocker):
    # arrange
    pg.get().fetch.return_value = future([
        {'offer_id': 888},
        {'offer_id': 999}
    ])
    expected = [888, 999]

    # act

    result = await get_offers_id_older_than(date=datetime(2020, 2, 24, 9, 0, 0, 303690, pytz.UTC),
                                            status_tab=enums.OfferStatusTab.deleted,
                                            limit=5)

    # assert
    assert result == expected
    pg.get().fetch.assert_called_once_with(
        'SELECT offer_id FROM offers where status_tab = $1 and updated_at <= $2 limit $3',
        'deleted',
        datetime(2020, 2, 24, 9, 0, 0, 303690, pytz.UTC),
        5,
    )
