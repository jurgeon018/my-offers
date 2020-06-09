import asyncio
from datetime import datetime

from cian_functional_test_utils.pytest_plugin import MockResponse


async def test_resend_offers(runner, monolith_cian_ms_announcements_mock, monolith_cian_elasticapi_mock, pg, logs):
    # arrange
    offer_id_1 = 111
    offer_id_2 = 222
    row_version = 1
    now = datetime.now()

    await pg.execute(
        """
        INSERT INTO offers_resender_cron (
            id,
            row_version,
            created_at
        )
        VALUES
            ($1, $2, $3)
        """,
        [
            1, row_version, now
        ]
    )
    await monolith_cian_ms_announcements_mock.add_stub(
        method='GET',
        path='/v1/get-changed-announcements-ids/',
        query={
            'rowVersion': row_version,
        },
        response=MockResponse(body={
                'offers_ids': [offer_id_1, offer_id_2]
            }
        ),
    )
    await monolith_cian_elasticapi_mock.add_stub(
        method='GET',
        path='/api/elastic/announcement/get/',
        query={
            'ids': [offer_id_1, offer_id_2]
        },
        response=MockResponse(body={
            'errors': [],
            'success': [
                {
                    'realty_object_id': offer_id_1,
                    'row_version': 2,
                },
                {
                    'realty_object_id': offer_id_2,
                    'row_version': 3,
                }
            ]
        }),
    )

    # act
    await runner.run_python_command('resend-offers')

    # assert
