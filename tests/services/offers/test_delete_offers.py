import freezegun
import pytest
import pytz
from cian_test_utils import future
from freezegun.api import FakeDatetime
from simple_settings.utils import settings_stub

from my_offers import enums
from my_offers.repositories.postgresql import tables
from my_offers.services.offers.delete_offers import delete_offers_data


class TestDeleteOffersService:
    @pytest.mark.gen_test
    @freezegun.freeze_time('2020-03-05 09:00:00.303690+00:00')
    async def test_right_params_in_get_offers_id_older_than(self, mocker):

        get_offers_id_older_than_mock = mocker.patch(
            'my_offers.services.offers.delete_offers.get_offers_id_older_than',
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
        get_offers_id_older_than_mock.assert_called_with(
            date=FakeDatetime(2020, 2, 24, 9, 0, 0, 303690, pytz.UTC),
            status_tab=enums.OfferStatusTab.deleted,
            limit=50,
        )

    @pytest.mark.gen_test
    async def test_has_data__process(self, mocker):
        offers_to_delete = [888, 999]
        get_offers_id_older_than_mock = mocker.patch(
            'my_offers.services.offers.delete_offers.get_offers_id_older_than',
            side_effect=[
                future(offers_to_delete),
                Exception(),
            ]
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
            )
        )

        # act
        with pytest.raises(Exception):
            await delete_offers_data()

        # assert
        get_offers_id_older_than_mock.assert_called()
        delete_rows_by_offer_id_mock.assert_has_calls([
            mocker.call(
                table=tables.offers,
                offer_ids=offers_to_delete
            ),
            mocker.call(
                table=tables.offers_billing_contracts,
                offer_ids=offers_to_delete
            ),
            mocker.call(
                table=tables.offers_last_import_error,
                offer_ids=offers_to_delete
            ),
            mocker.call(
                table=tables.offers_offences,
                offer_ids=offers_to_delete
            ),
            mocker.call(
                table=tables.offers_reindex_queue,
                offer_ids=offers_to_delete
            ),
            mocker.call(
                table=tables.offers_premoderations,
                offer_ids=offers_to_delete
            ),
        ])

    @pytest.mark.gen_test
    async def test_no_data__sleep(self, mocker):
        # arrange
        get_offers_id_older_than_mock = mocker.patch(
            'my_offers.services.offers.delete_offers.get_offers_id_older_than',
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
        get_offers_id_older_than_mock.assert_called()
        delete_rows_by_offer_id_mock.assert_not_called()
        sleep_mock.assert_called_with(77)
