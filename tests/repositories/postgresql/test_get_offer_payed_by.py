from cian_test_utils import future
from simple_settings.utils import settings_stub

from my_offers import pg
from my_offers.repositories.postgresql.offer import get_offers_payed_by


async def test_get_offers_payed_by():
    # arrange
    offer_ids = [1, 2, 3]
    pg.get().fetch.return_value = future([{
        'offer_id': 1,
        'master_user_id': 1,
        'user_id': 2,
        'payed_by': 3
    }])

    # act
    await get_offers_payed_by(offer_ids)

    # arrange
    with settings_stub(DB_TIMEOUT=3):
        pg.get().fetch.assert_called_once_with(
            '\n    select\n        offer_id,\n        '
            'master_user_id,\n        user_id,\n        payed_by\n    from\n        '
            'offers\n    where\n        offer_id = any($1::bigint[])\n    ',
            offer_ids,
            timeout=3
        )
