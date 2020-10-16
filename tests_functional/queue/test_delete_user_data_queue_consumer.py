import asyncio
from pathlib import Path


async def test_delete_user_data_queue_consumer(queue_service, pg, runner):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'clear_offers.sql')
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

    # act
    await runner.start_background_python_command('delete_user_data_queue_consumer')
    await queue_service.wait_consumer('my-offers.delete_user_data', timeout=300)
    await queue_service.publish('user-reporting.v1.deleted', {'operationId': '1', 'userId': 2994068}, exchange='users')
    await asyncio.sleep(1)

    # assert
    row = await pg.fetch('SELECT offer_id FROM offers_delete_queue')
    assert len(row) == 2
    row = await pg.fetch('SELECT * FROM agents_hierarchy')
    assert len(row) == 1
    row[0]['realty_user_id'] = 3
