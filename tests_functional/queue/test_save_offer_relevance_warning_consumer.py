import asyncio
from datetime import datetime, timedelta

import pytest
import pytz


@pytest.mark.parametrize(
    ('expected_message, expected_data'),
    (
        (
            {
                'realtyObjectId': 111,
                'checkStatusId': 'relevanceConfirmationRequired',
                'guid': '4228B2D9-C3E0-4D72-9EE6-96A9E678B96B',
                'relevance_type_message': 'warningOnly',
                'declineDate': datetime(2020, 5, 20, tzinfo=pytz.UTC).isoformat(),
                'date': datetime(2020, 4, 20, tzinfo=pytz.UTC).isoformat(),
            },
            {
                'offer_id': 111,
                'active': True,
                'check_id': '4228B2D9-C3E0-4D72-9EE6-96A9E678B96B',
                'due_date': None,
                'created_at': datetime(2020, 4, 20, tzinfo=pytz.UTC),
                'updated_at': datetime(2020, 4, 20, tzinfo=pytz.UTC),
            }
        ),
        (
            {
                'realtyObjectId': 222,
                'checkStatusId': 'relevanceConfirmationRequired',
                'guid': '73FBA463-B4EA-48DC-AF73-D5B9EE804E90',
                'relevance_type_message': 'willBeDeclined',
                'declineDate': datetime(2020, 5, 20, tzinfo=pytz.UTC).isoformat(),
                'date': datetime(2020, 4, 20, tzinfo=pytz.UTC).isoformat(),
            },
            {
                'offer_id': 222,
                'active': True,
                'check_id': '73FBA463-B4EA-48DC-AF73-D5B9EE804E90',
                'due_date': datetime(2020, 5, 20, tzinfo=pytz.UTC),
                'created_at': datetime(2020, 4, 20, tzinfo=pytz.UTC),
                'updated_at': datetime(2020, 4, 20, tzinfo=pytz.UTC),
            }
        ),
        (
            {
                'realtyObjectId': 333,
                'checkStatusId': 'relevanceConfirmed',
                'guid': '2188174A-43DC-4F04-BEEB-7E3E8DFB5112',
                'relevance_type_message': 'willBeDeclined',
                'declineDate': datetime(2020, 5, 20, tzinfo=pytz.UTC).isoformat(),
                'date': datetime(2020, 4, 20, tzinfo=pytz.UTC).isoformat(),
            },
            {
                'offer_id': 333,
                'active': False,
                'check_id': '2188174A-43DC-4F04-BEEB-7E3E8DFB5112',
                'due_date': datetime(2020, 5, 20, tzinfo=pytz.UTC),
                'created_at': datetime(2020, 4, 20, tzinfo=pytz.UTC),
                'updated_at': datetime(2020, 4, 20, tzinfo=pytz.UTC),
            }
        ),
    )
)
async def test_save_offer_relevance_warning_consumer__insert__expected(
    queue_service,
    pg,
    expected_message,
    expected_data,
):
    # arrange & act
    await queue_service.wait_consumer('my-offers.save_offer_relevance_warning')
    await queue_service.publish(
        'announcements-relevance-reporting.v1.changed',
        expected_message,
        exchange='moderation-announcements-relevance',
    )
    await asyncio.sleep(1)

    # assert
    row = await pg.fetchrow('SELECT * FROM offer_relevance_warnings ORDER BY offer_id DESC LIMIT 1')
    assert row == expected_data


async def test_save_offer_relevance_warning_consumer__insert_on_conflict__expected(
    queue_service,
    pg,
):
    # arrange
    offer_id = 209648847
    now = datetime.now(pytz.UTC)
    then = now - timedelta(days=1)
    await pg.execute(
        """
        INSERT INTO public.offer_relevance_warnings (
            offer_id,
            check_id,
            active,
            due_date,
            created_at,
            updated_at
        )
        VALUES
            ($1,  $2,  $3,  $4,  $5,  $6)
        """,
        [offer_id, '9D8183AD-9919-4535-94F1-6F0E801A1F3F', True, None, then, then],
    )

    message = {
        'realtyObjectId': offer_id,
        'checkStatusId': 'relevanceConfirmed',
        'guid': '52922E9B-53CE-4C16-88BE-108EE8518EE9',
        'relevance_type_message': 'willBeDeclined',
        'declineDate': datetime(2020, 5, 20, tzinfo=pytz.UTC).isoformat(),
        'date': now.isoformat(),
    }
    expected_data = {
        'offer_id': offer_id,
        'active': False,
        'check_id': '52922E9B-53CE-4C16-88BE-108EE8518EE9',
        'due_date': datetime(2020, 5, 20, tzinfo=pytz.UTC),
        'created_at': then,
        'updated_at': now,
    }

    # act
    await queue_service.wait_consumer('my-offers.save_offer_relevance_warning')
    await queue_service.publish(
        'announcements-relevance-reporting.v1.changed',
        message,
        exchange='moderation-announcements-relevance',
    )
    await asyncio.sleep(1)

    # assert
    row = await pg.fetchrow('SELECT * FROM offer_relevance_warnings WHERE offer_id = $1', [offer_id])
    assert row == expected_data


async def test_save_offer_relevance_warning_consumer__insert_on_conflict__skip_outdated(
    queue_service,
    pg,
):
    # arrange
    offer_id = 209746396
    now = datetime.now(pytz.UTC)
    then = now - timedelta(days=1)
    await pg.execute(
        """
        INSERT INTO public.offer_relevance_warnings (
            offer_id,
            check_id,
            active,
            due_date,
            created_at,
            updated_at
        )
        VALUES
            ($1,  $2,  $3,  $4,  $5,  $6)
        """,
        [offer_id, '9D8183AD-9919-4535-94F1-6F0E801A1F3F', True, None, then, now],
    )

    message = {
        'realtyObjectId': offer_id,
        'checkStatusId': 'relevanceConfirmed',
        'guid': '52922E9B-53CE-4C16-88BE-108EE8518EE9',
        'relevance_type_message': 'willBeDeclined',
        'declineDate': datetime(2020, 5, 20, tzinfo=pytz.UTC).isoformat(),
        'date': then.isoformat(),
    }
    expected_data = {
        'offer_id': offer_id,
        'active': True,
        'check_id': '9D8183AD-9919-4535-94F1-6F0E801A1F3F',
        'due_date': None,
        'created_at': then,
        'updated_at': now,
    }

    # act
    await queue_service.wait_consumer('my-offers.save_offer_relevance_warning')
    await queue_service.publish(
        'announcements-relevance-reporting.v1.changed',
        message,
        exchange='moderation-announcements-relevance',
    )
    await asyncio.sleep(1)

    # assert
    row = await pg.fetchrow('SELECT * FROM offer_relevance_warnings WHERE offer_id = $1', [offer_id])
    assert row == expected_data
