import asyncio
from datetime import datetime


async def test_save_agent_consumer__master_user_id_changed__changed_offer_master(
    pg,
    runner,
    queue_service
):
    # arrange
    now = datetime.now()

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

    await pg.execute(
        """
        INSERT INTO offers (
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
            ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15)
        """,
        [
            1, 2, 2994068, 'sale', 'flat', 'notActive', [], True, False, False, 'text',
            '{"id": 11, "category": "flatSale", "status": "Draft"}',
            1, now, now
        ]
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
    rows_agents = await pg.fetch('select * from agents_hierarchy')
    rows_offers = await pg.fetch('select * from offers')
    assert len(rows_agents) == 1
    assert len(rows_offers) == 1

    row_agent = rows_agents[0]
    row_offer = rows_offers[0]
    assert row_agent['id'] == 3
    assert row_agent['row_version'] == 4
    assert row_agent['realty_user_id'] == 2994068
    assert row_agent['master_agent_user_id'] == 5
    assert row_offer['master_user_id'] == 5


async def test_save_agent_consumer__no_master_agent_user_id__changed_offer_master(
    pg,
    runner,
    queue_service
):
    # arrange
    now = datetime.now()

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

    await pg.execute(
        """
        INSERT INTO offers (
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
            1, 2, 2994068, 'sale', 'flat', 'notActive', [], True, False, False, 'text',
            '{"id": 11, "category": "flatSale", "status": "Draft"}',
            1, now, now,
            2, 2, 2994068, 'rent', 'flat', 'notActive', [], True, False, False, 'text',
            '{"id": 11, "category": "flatRent", "status": "Draft"}',
            1, now, now
        ]
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
            'masterAgentUserId': None,
        },
    )
    await asyncio.sleep(1)

    # assert
    rows_agents = await pg.fetch('select * from agents_hierarchy')
    rows_offers = await pg.fetch('select * from offers')
    assert len(rows_agents) == 1
    assert len(rows_offers) == 2

    row_agent = rows_agents[0]
    assert row_agent['id'] == 3
    assert row_agent['row_version'] == 4
    assert row_agent['realty_user_id'] == 2994068
    assert row_agent['master_agent_user_id'] is None
    assert rows_offers[0]['master_user_id'] == 2994068
    assert rows_offers[1]['master_user_id'] == 2994068
