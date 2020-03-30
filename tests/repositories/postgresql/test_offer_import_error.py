from datetime import datetime

import pytest
from cian_test_utils import future

from my_offers import pg
from my_offers.entities import OfferImportError
from my_offers.repositories.postgresql.offer_import_error import get_last_import_errors, upsert_offer_import_errors


@pytest.mark.gen_test
async def test_upsert_offer_import_errors(mocker):
    # arrange
    errors = [
        OfferImportError(
            offer_id=222,
            type='yyy',
            message='ffff',
            created_at=datetime(2020, 3, 5, 0, 0)
        ),
        OfferImportError(
            offer_id=333,
            type='bbb',
            message='aaaa',
            created_at=datetime(2020, 3, 7, 0, 0)
        ),
    ]

    # act
    await upsert_offer_import_errors(errors)

    # assert
    pg.get().execute.assert_called_once_with(
        'INSERT INTO offers_last_import_error (offer_id, type, message, created_at) '
        'VALUES ($5, $7, $3, $1), ($6, $8, $4, $2) ON CONFLICT (offer_id) DO '
        'UPDATE SET type = excluded.type, message = excluded.message, created_at = excluded.created_at '
        'WHERE offers_last_import_error.created_at < excluded.created_at',
        datetime(2020, 3, 5, 0, 0),
        datetime(2020, 3, 7, 0, 0),
        'ffff',
        'aaaa',
        222,
        333,
        'yyy',
        'bbb',
    )


@pytest.mark.gen_test
async def test_get_last_import_errors(mocker):
    # arrange
    pg.get().fetch.return_value = future([
        {'offer_id': 11, 'message': 'fff'},
        {'offer_id': 22, 'message': 'bb'},
    ])

    expected = {11: 'fff', 22: 'bb'}

    # act
    result = await get_last_import_errors([11, 22])

    # assert
    assert result == expected
    pg.get().fetch.assert_called_once_with(
        '\n        SELECT\n            offer_id,\n            message\n        '
        'FROM\n            offers_last_import_error\n        WHERE\n            offer_id = ANY($1::BIGINT[])\n    ',
        [11, 22]
    )
