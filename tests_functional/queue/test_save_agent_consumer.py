import asyncio


async def test_save_agent_consumer__row_version_mismatch__discard_changes(pg, runner, queue_service, logs):
    # arrange
    await pg.execute(
        """
        INSERT INTO agents_hierarchy (
            id,
            row_version,
            realty_user_id,
            master_agent_user_id,
            created_at,
            updated_at
        )
        VALUES
            (1, 1, 1, 2994068, current_timestamp, current_timestamp),
            (2, 2, 2994068, 2, current_timestamp, current_timestamp),
            (3, 3, 3, null, current_timestamp, current_timestamp)
        """,
    )
    await runner.start_background_python_command('save_agent_consumer')
    await queue_service.wait_consumer('my-offers.save_agent', timeout=300)

    # act
    await queue_service.publish(
        exchange='users',
        routing_key='agent-reporting.v1.changed',
        payload={
            'operationId': '1',
            'id': 1,
            'rowVersion': 2,
            'realtyUserId': 2994068,
        },
    )
    await asyncio.sleep(1)

    # assert
    assert 'discard agent changes' in logs.get()


async def test_save_agent_consumer__row_version_is_greater__remove_old_and_save_new(pg, runner, queue_service):
    # arrange
    await pg.execute(
        """
        INSERT INTO agents_hierarchy (
            id,
            row_version,
            realty_user_id,
            master_agent_user_id,
            created_at,
            updated_at
        )
        VALUES
            (1, 1, 1, 2994068, current_timestamp, current_timestamp),
            (2, 2, 2994068, 2, current_timestamp, current_timestamp),
            (3, 3, 3, null, current_timestamp, current_timestamp)
        """,
    )
    await runner.start_background_python_command('save_agent_consumer')
    await queue_service.wait_consumer('my-offers.save_agent', timeout=300)

    # act
    await queue_service.publish(
        exchange='users',
        routing_key='agent-reporting.v1.changed',
        payload={
            'operationId': '1',
            'id': 3,
            'rowVersion': 4,
            'realtyUserId': 2994068,
            'masterAgentUserId': 5,
        },
    )
    await asyncio.sleep(1)

    # assert
    rows = await pg.fetch('select * from agents_hierarchy')
    assert len(rows) == 1

    row = rows[0]
    assert row['id'] == 3
    assert row['row_version'] == 4
    assert row['realty_user_id'] == 2994068
    assert row['master_agent_user_id'] == 5
