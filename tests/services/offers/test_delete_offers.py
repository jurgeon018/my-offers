import asyncio

import freezegun
import pytest
from cian_test_utils import future
from simple_settings.utils import settings_stub

from my_offers.repositories.postgresql import tables
from my_offers.repositories.postgresql.offers_delete_queue import offers_delete_queue
from my_offers.repositories.postgresql.offers_duplicates import offers_duplicates
from my_offers.services.offers.delete_offers import delete_offers_data


class TestDeleteOffersService:
    @pytest.mark.gen_test
    @freezegun.freeze_time('2020-03-05 09:00:00.303690+00:00')
    async def test_right_params_in_get_offers_id_older_than(self, mocker):

        get_offer_ids_for_delete_mock = mocker.patch(
            'my_offers.services.offers.delete_offers.postgresql.get_offer_ids_for_delete',
            side_effect=[
                future([888, 999]),
                Exception(),
            ]
        )

        # act
        with settings_stub(
                COUNT_DAYS_HOLD_DELETED_OFFERS=10,
                COUNT_OFFERS_DELETE_IN_ONE_TIME=50
        ), pytest.raises(Exception):
            await delete_offers_data()

        # assert
        get_offer_ids_for_delete_mock.assert_called_with(
            limit=50,
            timeout=30,
        )

    @pytest.mark.gen_test
    async def test_has_data__process(self, mocker):
        offers_to_delete = [888, 999]
        get_offer_ids_for_delete_mock = mocker.patch(
            'my_offers.services.offers.delete_offers.postgresql.get_offer_ids_for_delete',
            side_effect=[
                future(offers_to_delete),
                Exception(),
            ]
        )
        delete_offers_mock = mocker.patch(
            'my_offers.services.offers.delete_offers.postgresql.delete_offers',
            return_value=future(offers_to_delete),
        )

        delete_rows_by_offer_id_mock = mocker.patch(
            'my_offers.services.offers.delete_offers.delete_rows_by_offer_id',
            side_effect=(
                future(),
                future(),
                future(),
                future(),
                future(),
                future(),
                future(),
            )
        )

        # act
        with pytest.raises(Exception):
            await delete_offers_data()

        # assert
        get_offer_ids_for_delete_mock.assert_called()
        delete_offers_mock.assert_called_once_with(
            offer_ids=offers_delete_queue,
            timeout=30,
        )
        delete_rows_by_offer_id_mock.assert_has_calls([
            mocker.call(
                table=offers_delete_queue,
                offer_ids=offers_to_delete,
                timeout=30,
            ),
            mocker.call(
                table=tables.offers_billing_contracts,
                offer_ids=offers_to_delete,
                timeout=30,
            ),
            mocker.call(
                table=offers_duplicates,
                offer_ids=offers_to_delete,
                timeout=30,
            ),
            mocker.call(
                table=tables.offers_last_import_error,
                offer_ids=offers_to_delete,
                timeout=30,
            ),
            mocker.call(
                table=tables.offers_offences,
                offer_ids=offers_to_delete,
                timeout=30,
            ),
            mocker.call(
                table=tables.offers_premoderations,
                offer_ids=offers_to_delete,
                timeout=30,
            ),
            mocker.call(
                table=tables.offers_reindex_queue,
                offer_ids=offers_to_delete,
                timeout=30,
            ),
        ])

    @pytest.mark.gen_test
    async def test_no_data__sleep(self, mocker):
        # arrange
        get_offer_ids_for_delete_mock = mocker.patch(
            'my_offers.services.offers.delete_offers.postgresql.get_offer_ids_for_delete',
            side_effect=[
                future(None),
                Exception(),
            ]
        )
        delete_rows_by_offer_id_mock = mocker.patch(
            'my_offers.services.offers.delete_offers.delete_rows_by_offer_id',
            return_value=future(None)
        )

        sleep_mock = mocker.patch(
            'my_offers.services.offers.delete_offers.asyncio.sleep',
            return_value=future(None)
        )

        # act
        with pytest.raises(Exception), settings_stub(TIMEOUT_BETWEEN_DELETE_OFFERS=77):
            await delete_offers_data()

        # assert
        get_offer_ids_for_delete_mock.assert_called()
        delete_rows_by_offer_id_mock.assert_not_called()
        sleep_mock.assert_called_with(77)

    @pytest.mark.gen_test
    async def test_timeout__sleep(self, mocker):
        # arrange
        get_offer_ids_for_delete_mock = mocker.patch(
            'my_offers.services.offers.delete_offers.postgresql.get_offer_ids_for_delete',
            side_effect=[
                asyncio.exceptions.TimeoutError(),
                Exception(),
            ]
        )
        delete_rows_by_offer_id_mock = mocker.patch(
            'my_offers.services.offers.delete_offers.delete_rows_by_offer_id',
            return_value=future(None)
        )

        sleep_mock = mocker.patch(
            'my_offers.services.offers.delete_offers.asyncio.sleep',
            return_value=future(None)
        )

        # act
        with pytest.raises(Exception), settings_stub(TIMEOUT_BETWEEN_DELETE_OFFERS=77):
            await delete_offers_data()

        # assert
        get_offer_ids_for_delete_mock.assert_called()
        delete_rows_by_offer_id_mock.assert_not_called()
        sleep_mock.assert_called_with(77)
