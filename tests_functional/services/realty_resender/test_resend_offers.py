import uuid
from datetime import datetime

from cian_functional_test_utils.pytest_plugin import MockResponse


async def test_resend_offers__different_row_versions(
        runner,
        monolith_cian_elasticapi_mock,
        pg,
        logs,
        queue_service,
):
    # arrange
    offer_id_1 = 111
    offer_id_2 = 222
    row_version = 1
    operation_id = str(uuid.uuid1())
    now = datetime.now()

    await pg.execute(
        """
        INSERT INTO offers_resender_cron (
            operation_id,
            row_version,
            created_at
        )
        VALUES
            ($1, $2, $3)
        """,
        [
            operation_id, row_version, now
        ]
    )
    await pg.execute(
        """
        INSERT INTO public.offers (
            offer_id,
            master_user_id,
            user_id,
            deal_type,
            offer_type,
            status_tab,
            services,
            is_manual,
            is_in_hidden_base,
            has_photo,
            search_text,
            raw_data,
            row_version,
            created_at,
            updated_at
        )
        VALUES
            ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15),
            ($16, $17, $18, $19, $20, $21, $22, $23, $24, $25, $26, $27, $28, $29, $30)
        """,
        [
            offer_id_1, 2, 2, 'sale', 'flat', 'active', [], True, False, False, 'text', '{}', 9999999, now, now,
            offer_id_2, 2, 3, 'sale', 'flat', 'active', [], True, False, False, 'text', '{}', 1, now, now,
        ]
    )
    await monolith_cian_elasticapi_mock.add_stub(
        method='GET',
        path='/api/elastic/announcement/v3/get-changed-ids/',
        query={
            'rowVersion': row_version,
        },
        response=MockResponse(body=[
            {
                'realty_object_id': offer_id_1,
                'row_version': 2,
            },
            {
                'realty_object_id': offer_id_2,
                'row_version': 33333333,
            }
        ])
    )
    await monolith_cian_elasticapi_mock.add_stub(
        method='GET',
        path='/api/elastic/announcement/get/',
        # query={
        #     'ids': [offer_id_2]
        # },
        response=MockResponse(body={
            'errors': [],
            'success': [
                {
                    'objectModel': ('{"id": 222, "userId": 444, "publishedUserId": 444,  "rowVersion": 100002, '
                                    '"category": "officeRent", "bargainTerms": {}, "phones": [], "status": "Draft"}'),
                }
            ]
        })
    )
    queue = await queue_service.make_tmp_queue(routing_key='my-offers.resend.v1.new')

    # act
    await runner.run_python_command('resend-offers')

    # assert
    messages = await queue.get_messages()
    assert len(messages) == 1

    next_session = await pg.fetchrow('SELECT * FROM offers_resender_cron ORDER BY id DESC LIMIT 1')
    first_stats = await pg.fetchrow('SELECT * FROM offers_resender_stats LIMIT 1')

    next_session.pop('operation_id')
    next_session.pop('created_at')
    assert next_session == {
        'id': 2,
        'row_version': 33332333,
    }
    first_stats.pop('operation_id')
    first_stats.pop('created_at')
    assert first_stats == {
        'founded_from_elastic': 2,
        'need_update': 1,
        'not_found_in_db': 0,
    }
    assert 'Get changed offers from row_version: 1, count: 2' in logs.get()
    assert 'Get offers diff, progress 2/2' in logs.get()


async def test_resend_offers__use_elastic_api(
        runner,
        monolith_cian_elasticapi_mock,
        pg,
        logs,
        queue_service,
):
    # arrange
    offer_id_1 = 111
    offer_id_2 = 222
    row_version = 1
    operation_id = str(uuid.uuid1())
    now = datetime.now()

    await pg.execute(
        """
        INSERT INTO offers_resender_cron (
            operation_id,
            row_version,
            created_at
        )
        VALUES
            ($1, $2, $3)
        """,
        [
            operation_id, row_version, now
        ]
    )
    await monolith_cian_elasticapi_mock.add_stub(
        method='GET',
        path='/api/elastic/announcement/v3/get-changed-ids/',
        query={
            'rowVersion': row_version,
        },
        response=MockResponse(body=[
            {
                'realty_object_id': offer_id_1,
                'row_version': 2,
            },
            {
                'realty_object_id': offer_id_2,
                'row_version': 3,
            }
        ])
    )
    await monolith_cian_elasticapi_mock.add_stub(
        method='GET',
        path='/api/elastic/announcement/get/',
        query={
            'ids': [offer_id_1, offer_id_2],
        },
        response=MockResponse(body={
            'errors': [],
            'success': [
                {
                    'objectModel': ('{"id": 111, "userId": 123, "publishedUserId": 123,  "rowVersion": 100001, '
                                    '"category": "officeRent", "bargainTerms": {}, "phones": [], "status": "Draft"}'),
                },
                {
                    'objectModel': ('{"id": 222, "userId": 444, "publishedUserId": 444,  "rowVersion": 100002, '
                                    '"category": "officeRent", "bargainTerms": {}, "phones": [], "status": "Draft"}'),
                }
            ]
        })
    )
    queue = await queue_service.make_tmp_queue(routing_key='my-offers.resend.v1.new')

    # act
    await runner.run_python_command('resend-offers')

    # assert
    messages = await queue.get_messages()
    assert len(messages) == 2

    next_session = await pg.fetchrow('SELECT * FROM offers_resender_cron ORDER BY id DESC LIMIT 1')
    first_stats = await pg.fetchrow('SELECT * FROM offers_resender_stats LIMIT 1')

    next_session.pop('operation_id')
    next_session.pop('created_at')
    assert next_session == {
        'id': 2,
        'row_version': -997,
    }
    first_stats.pop('operation_id')
    first_stats.pop('created_at')
    assert first_stats == {
        'founded_from_elastic': 2,
        'need_update': 0,
        'not_found_in_db': 2,
    }
    assert 'Get changed offers from row_version: 1, count: 2' in logs.get()
    assert 'Get offers diff, progress 2/2' in logs.get()


async def test_resend_offers__use_realty_task(
        runner,
        monolith_cian_elasticapi_mock,
        monolith_cian_realty_mock,
        pg,
        logs,
        runtime_settings
):
    # arrange
    offer_id_1 = 111
    offer_id_2 = 222
    row_version = 1
    operation_id = str(uuid.uuid1())
    now = datetime.now()
    job_id = 999999

    await pg.execute(
        """
        INSERT INTO offers_resender_cron (
            operation_id,
            row_version,
            created_at
        )
        VALUES
            ($1, $2, $3)
        """,
        [
            operation_id, row_version, now
        ]
    )
    await monolith_cian_elasticapi_mock.add_stub(
        method='GET',
        path='/api/elastic/announcement/v3/get-changed-ids/',
        query={
            'rowVersion': row_version,
        },
        response=MockResponse(body=[
            {
                'realty_object_id': offer_id_1,
                'row_version': 2,
            },
            {
                'realty_object_id': offer_id_2,
                'row_version': 3,
            }
        ])
    )
    await runtime_settings.set({'SYNC_OFFERS_ALLOW_RUN_TASK': True})
    await monolith_cian_realty_mock.add_stub(
        method='POST',
        path='/api/v1/resend-reporting-messages/resend-announcements/',
        body={
            'ids': [offer_id_1, offer_id_2],
            'comment': '',
            'broadcastType': 'temp'
        },
        response=MockResponse(body={'id': job_id})
    )
    await monolith_cian_realty_mock.add_stub(
        method='GET',
        path='/api/v1/resend-reporting-messages/get-job/',
        query={
            'id': job_id
        },
        response=[
            MockResponse(
                body={
                    'state': 'active'
                },
                repeat=3
            ),
            MockResponse(
                body={
                    'state': 'finished',
                    'data': {
                        'ids': [offer_id_1, offer_id_1],
                        'successIds': [offer_id_1, offer_id_1],
                        'errorIds': [],
                    }
                }
            ),
        ]
    )

    # act
    await runner.run_python_command('resend-offers')

    # assert
    next_session = await pg.fetchrow('SELECT * FROM offers_resender_cron ORDER BY id DESC LIMIT 1')
    first_stats = await pg.fetchrow('SELECT * FROM offers_resender_stats LIMIT 1')

    next_session.pop('operation_id')
    next_session.pop('created_at')
    assert next_session == {
        'id': 2,
        'row_version': -997,
    }
    first_stats.pop('operation_id')
    first_stats.pop('created_at')
    assert first_stats == {
        'founded_from_elastic': 2,
        'need_update': 0,
        'not_found_in_db': 2,
    }
    assert 'Get changed offers from row_version: 1, count: 2' in logs.get()
    assert 'Get offers diff, progress 2/2' in logs.get()


async def test_resend_offers__use_elastic_api__errors_warning(
        runner,
        monolith_cian_elasticapi_mock,
        pg,
        logs,
        queue_service,
):
    # arrange
    offer_id_1 = 111
    offer_id_2 = 222
    row_version = 1
    operation_id = str(uuid.uuid1())
    now = datetime.now()

    await pg.execute(
        """
        INSERT INTO offers_resender_cron (
            operation_id,
            row_version,
            created_at
        )
        VALUES
            ($1, $2, $3)
        """,
        [
            operation_id, row_version, now
        ]
    )
    await monolith_cian_elasticapi_mock.add_stub(
        method='GET',
        path='/api/elastic/announcement/v3/get-changed-ids/',
        query={
            'rowVersion': row_version,
        },
        response=MockResponse(body=[
            {
                'realty_object_id': offer_id_1,
                'row_version': 2,
            },
            {
                'realty_object_id': offer_id_2,
                'row_version': 3,
            }
        ])
    )
    await monolith_cian_elasticapi_mock.add_stub(
        method='GET',
        path='/api/elastic/announcement/get/',
        query={
            'ids': [offer_id_1, offer_id_2],
        },
        response=MockResponse(body={
            'errors': [
                {
                    'code': 'announcements_not_found',
                    'message': 'kek',
                    'realty_object_id': offer_id_1,
                }
            ],
            'success': [
                {
                    'objectModel': ('{"id": 222, "userId": 444, "publishedUserId": 444,  "rowVersion": 100002, '
                                    '"category": "officeRent", "bargainTerms": {}, "phones": [], "status": "Draft"}'),
                }
            ]
        })
    )

    queue = await queue_service.make_tmp_queue(routing_key='my-offers.resend.v1.new')

    # act
    await runner.run_python_command('resend-offers')

    # assert
    messages = await queue.get_messages()
    assert len(messages) == 1

    next_session = await pg.fetchrow('SELECT * FROM offers_resender_cron ORDER BY id DESC LIMIT 1')
    first_stats = await pg.fetchrow('SELECT * FROM offers_resender_stats LIMIT 1')

    next_session.pop('operation_id')
    next_session.pop('created_at')
    assert next_session == {
        'id': 2,
        'row_version': -997,
    }
    first_stats.pop('operation_id')
    first_stats.pop('created_at')
    assert first_stats == {
        'founded_from_elastic': 2,
        'need_update': 0,
        'not_found_in_db': 2,
    }
    assert 'Get changed offers from row_version: 1, count: 2' in logs.get()
    assert 'Get offers diff, progress 2/2' in logs.get()
    assert 'Error during call offers from elasticapi' in logs.get()


async def test_resend_offers__use_realty_task__errors_warning(
        runner,
        monolith_cian_elasticapi_mock,
        monolith_cian_realty_mock,
        pg,
        logs,
        runtime_settings
):
    # arrange
    offer_id_1 = 111
    offer_id_2 = 222
    row_version = 1
    operation_id = str(uuid.uuid1())
    now = datetime.now()
    job_id = 999999

    await pg.execute(
        """
        INSERT INTO offers_resender_cron (
            operation_id,
            row_version,
            created_at
        )
        VALUES
            ($1, $2, $3)
        """,
        [
            operation_id, row_version, now
        ]
    )
    await monolith_cian_elasticapi_mock.add_stub(
        method='GET',
        path='/api/elastic/announcement/v3/get-changed-ids/',
        query={
            'rowVersion': row_version,
        },
        response=MockResponse(body=[
            {
                'realty_object_id': offer_id_1,
                'row_version': 2,
            },
            {
                'realty_object_id': offer_id_2,
                'row_version': 3,
            }
        ])
    )
    await runtime_settings.set({'SYNC_OFFERS_ALLOW_RUN_TASK': True})
    await monolith_cian_realty_mock.add_stub(
        method='POST',
        path='/api/v1/resend-reporting-messages/resend-announcements/',
        body={
            'ids': [offer_id_1, offer_id_2],
            'comment': '',
            'broadcastType': 'temp'
        },
        response=MockResponse(body={'id': job_id})
    )
    await monolith_cian_realty_mock.add_stub(
        method='GET',
        path='/api/v1/resend-reporting-messages/get-job/',
        query={
            'id': job_id
        },
        response=MockResponse(
            body={
                'state': 'finished',
                'data': {
                    'ids': [offer_id_1, offer_id_2],
                    'successIds': [offer_id_2],
                    'errorIds': [offer_id_1],
                }
            }
        ),
    )

    # act
    await runner.run_python_command('resend-offers')

    # assert
    assert 'Get changed offers from row_version: 1, count: 2' in logs.get()
    assert 'Get offers diff, progress 2/2' in logs.get()
    assert f'Error during resend offers: [{offer_id_1}]' in logs.get()
