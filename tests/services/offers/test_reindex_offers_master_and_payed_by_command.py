from datetime import datetime

from cian_test_utils import future
from simple_settings.utils import settings_stub

from my_offers.entities import ReindexOfferItem
from my_offers.services.offers._reindex_offers_master_and_payed_by import reindex_offers_master_and_payed_by_command


PATH = 'my_offers.services.offers._reindex_offers_master_and_payed_by.'


async def test_reindex_offers_master_and_payed_by_command(mocker):
    # arrange
    get_reindex_items_mock = mocker.patch(
        f'{PATH}get_reindex_items',
        side_effect=[
            future([
                ReindexOfferItem(offer_id=11, created_at=datetime(2020, 3, 12), sync=True),
            ]),
            future([
                ReindexOfferItem(offer_id=12, created_at=datetime(2020, 3, 12)),
            ]),
            future([])
        ]
    )

    update_offers_master_user_id_and_payed_by_mock = mocker.patch(
        f'{PATH}update_offers_master_user_id_and_payed_by',
        return_value=future()
    )

    delete_reindex_items_mock = mocker.patch(
        f'{PATH}delete_reindex_items',
        return_value=future()
    )

    sleep_mock = mocker.patch(
        'asyncio.sleep',
        return_value=future()
    )

    # act
    with settings_stub(
        REINDEX_CHUNK=1,
        REINDEX_TIMEOUT=3
    ):
        await reindex_offers_master_and_payed_by_command()

    # assert
    get_reindex_items_mock.assert_has_calls([
        mocker.call(1),
        mocker.call(1),
        mocker.call(1)
    ])
    update_offers_master_user_id_and_payed_by_mock.assert_has_calls([
        mocker.call([11]),
        mocker.call([12])
    ])
    delete_reindex_items_mock.assert_has_calls([
        mocker.call([11]),
        mocker.call([12])
    ])
    sleep_mock.assert_has_calls([
        mocker.call(3),
        mocker.call(3)
    ])
