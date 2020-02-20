from datetime import datetime

import pytest
from cian_test_utils import future

from my_offers import pg, enums
from my_offers.entities import Offer
from my_offers.repositories.monolith_cian_announcementapi.entities.publish_term import Services
from my_offers.repositories.postgresql.offer import get_offer_by_id


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
        )
    )
)
async def test_get_offer_by_id(mocker, row, expected):
    # arrange
    mocker.patch('my_offers.repositories.postgresql.offer_mapper.map_from', return_value=expected)
    pg.get().fetchrow.return_value = future(row)

    # act
    result = await get_offer_by_id(111)

    # assert
    assert result == expected
