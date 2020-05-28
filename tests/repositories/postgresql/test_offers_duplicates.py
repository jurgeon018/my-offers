import freezegun
import pytest
import pytz
from cian_test_utils import future
from freezegun.api import FakeDatetime

from my_offers import pg
from my_offers.repositories.offers_duplicates.entities import Duplicate
from my_offers.repositories.postgresql import delete_offers_duplicates, update_offers_duplicates


@pytest.mark.gen_test
@freezegun.freeze_time('2020-05-13')
async def test_update_offers_duplicates(mocker):
    # arrange
    duplicates = [Duplicate(1, 2), Duplicate(2, 2)]
    pg.get().fetch.return_value = future([{
        'offer_id': 1,
        'updated_at': None,
    }])

    # act
    result = await update_offers_duplicates(duplicates)

    # assert
    pg.get().fetch.assert_called_once_with(
        'INSERT INTO offers_duplicates (offer_id, group_id, created_at) VALUES ($5, $3, $1), ($6, $4, $2) '
        'ON CONFLICT (offer_id) DO UPDATE SET group_id = excluded.group_id, updated_at = excluded.created_at '
        'RETURNING offers_duplicates.offer_id, offers_duplicates.updated_at',
        FakeDatetime(2020, 5, 13, 0, 0, tzinfo=pytz.UTC),
        FakeDatetime(2020, 5, 13, 0, 0, tzinfo=pytz.UTC),
        1,
        2,
        2,
        2,
    )

    assert result == [1]


@freezegun.freeze_time('2020-05-13')
async def test_update_offers_duplicates__not_update__empty(mocker):
    # arrange
    duplicates = [Duplicate(1, 2), Duplicate(2, 2)]
    pg.get().fetch.return_value = future([])

    # act
    result = await update_offers_duplicates(duplicates)

    # assert
    pg.get().fetch.assert_called_once_with(
        'INSERT INTO offers_duplicates (offer_id, group_id, created_at) VALUES ($5, $3, $1), ($6, $4, $2) '
        'ON CONFLICT (offer_id) DO UPDATE SET group_id = excluded.group_id, updated_at = excluded.created_at '
        'RETURNING offers_duplicates.offer_id, offers_duplicates.updated_at',
        FakeDatetime(2020, 5, 13, 0, 0, tzinfo=pytz.UTC),
        FakeDatetime(2020, 5, 13, 0, 0, tzinfo=pytz.UTC),
        1,
        2,
        2,
        2,
    )

    assert result == []


@pytest.mark.gen_test
async def test_delete_offers_duplicates(mocker):
    # arrange & act
    await delete_offers_duplicates([1, 2])

    # assert
    pg.get().execute.assert_called_once_with(
        'DELETE FROM offers_duplicates WHERE offer_id = ANY($1::BIGINT[])',
        [1, 2],
    )
