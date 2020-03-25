import pytest
from cian_test_utils import future
from simple_settings.utils import settings_stub

from my_offers.services.offers.delete_offers import delete_offers_data


class TestDeleteOffersService:
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
        delete_offers_by_id_mock = mocker.patch(
            'my_offers.services.offers.delete_offers.delete_offers_by_id',
            return_value=future(None)
        )
        delete_contracts_by_offer_id_mock = mocker.patch(
            'my_offers.services.offers.delete_offers.delete_contracts_by_offer_id',
            return_value=future(None)
        )
        delete_import_errors_by_offer_id_mock = mocker.patch(
            'my_offers.services.offers.delete_offers.delete_import_errors_by_offer_id',
            return_value=future(None)
        )
        delete_offers_offence_by_offer_id_mock = mocker.patch(
            'my_offers.services.offers.delete_offers.delete_offers_offence_by_offer_id',
            return_value=future(None)
        )
        delete_reindex_items_mock = mocker.patch(
            'my_offers.services.offers.delete_offers.delete_reindex_items',
            return_value=future(None)
        )

        # act
        with pytest.raises(Exception):
            await delete_offers_data()

        # assert
        get_offers_id_older_than_mock.assert_called()
        delete_contracts_by_offer_id_mock.assert_called_once_with(offers_to_delete)
        delete_offers_by_id_mock.assert_called_once_with(offers_to_delete)
        delete_import_errors_by_offer_id_mock.assert_called_once_with(offers_to_delete)
        delete_offers_offence_by_offer_id_mock.assert_called_once_with(offers_to_delete)
        delete_reindex_items_mock.assert_called_once_with(offers_to_delete)

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
        delete_offers_by_id_mock = mocker.patch(
            'my_offers.services.offers.delete_offers.delete_offers_by_id',
            return_value=future(None)
        )
        delete_contracts_by_offer_id_mock = mocker.patch(
            'my_offers.services.offers.delete_offers.delete_contracts_by_offer_id',
            return_value=future(None)
        )
        delete_import_errors_by_offer_id_mock = mocker.patch(
            'my_offers.services.offers.delete_offers.delete_import_errors_by_offer_id',
            return_value=future(None)
        )
        delete_offers_offence_by_offer_id_mock = mocker.patch(
            'my_offers.services.offers.delete_offers.delete_offers_offence_by_offer_id',
            return_value=future(None)
        )
        delete_reindex_items_mock = mocker.patch(
            'my_offers.services.offers.delete_offers.delete_reindex_items',
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
        delete_offers_by_id_mock.assert_not_called()
        delete_contracts_by_offer_id_mock.assert_not_called()
        delete_import_errors_by_offer_id_mock.assert_not_called()
        delete_offers_offence_by_offer_id_mock.assert_not_called()
        delete_reindex_items_mock.assert_not_called()
        sleep_mock.assert_called_with(77)
