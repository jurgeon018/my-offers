from datetime import datetime

import pytest
from cian_test_utils import future

from my_offers.entities import OfferImportError
from my_offers.services.offers_import import save_offers_import_error


@pytest.mark.gen_test
async def test_save_offers_import_error(mocker):
    # arrange
    errors = [
        OfferImportError(
            offer_id=111,
            type='yyy',
            message='ffff',
            created_at=datetime(2020, 3, 5)
        )
    ]
    upsert_offer_import_errors_mock = mocker.patch(
        'my_offers.services.offers_import._save_offers_import_error.upsert_offer_import_errors',
        return_value=future()
    )

    # act
    await save_offers_import_error(errors)

    # assert
    upsert_offer_import_errors_mock.assert_called_once_with(errors)
