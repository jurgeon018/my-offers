import pytest
from cian_test_utils import future

from my_offers import pg
from my_offers.entities.get_offers import OfferCounters
from my_offers.repositories.postgresql.offer import get_offer_counters


@pytest.mark.gen_test
async def test_get_offer_counters(mocker):
    # arrange
    rows = [
        {'status_tab': 'active', 'cnt': 11},
        {'status_tab': 'not_active', 'cnt': 0},
        {'status_tab': 'zzzz', 'cnt': 1000},
    ]

    expected = OfferCounters(
        active=11,
        not_active=0,
        declined=0,
        archived=None,
    )

    pg.get().fetch.return_value = future(rows)

    # act
    result = await get_offer_counters(111)

    # assert
    assert result == expected

    pg.get().fetch.assert_called_once_with(
        '\n        select\n            status_tab,\n            count(*) as cnt\n        '
        'from\n            offers\n'
        '        where\n            master_user_id = $1\n        group by\n            status_tab\n    ',
        111
    )
