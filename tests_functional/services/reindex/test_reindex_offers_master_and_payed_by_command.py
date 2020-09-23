from datetime import datetime
from pathlib import Path

import asyncio
import pytz


async def test_reindex_offers_master_and_payed_by_command_update_for_agent_self_payed(runner, pg):
    now = datetime.now(pytz.utc)
    offer_id = 209194477
    user_id = old_master_user_id = 29437831
    new_master_user_id = 29437832

    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')
    await pg.execute(
        """
        INSERT INTO public.agents_hierarchy (
           id,
           row_version,
           realty_user_id,
           master_agent_user_id,
           created_at,
           updated_at
        )
        VALUES
           ($1, $2, $3, $4, $5, $6),
           ($7, $8, $9, $10, $11, $12)
        """,
        [
            1, 1, user_id, new_master_user_id, now, now,
            2, 1, new_master_user_id, None, now, now,
        ]
    )

    await pg.execute(
        """
        INSERT INTO public.offers_billing_contracts (
           id,
           user_id,
           actor_user_id,
           publisher_user_id,
           offer_id,
           start_date,
           payed_till,
           row_version,
           is_deleted,
           created_at,
           updated_at
        )
        VALUES
           ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
        """,
        [
            1, 1, 1, user_id, offer_id, now, now, 1, False, now, now
        ]
    )

    await pg.execute(
        """
        INSERT INTO offers_reindex_queue(offer_id, created_at)
        VALUES
            ($1, current_timestamp)
        """,
        [offer_id]
    )

    # act
    await runner.start_background_python_command('reindex-offers-master-and-payed-by')
    await asyncio.sleep(2)

    # assert
    row = await pg.fetchrow('SELECT * FROM offers WHERE offer_id = $1', [offer_id])

    assert row['master_user_id'] == new_master_user_id
    assert row['old_master_user_id'] == old_master_user_id
    assert row['payed_by'] == user_id


async def test_reindex_offers_master_and_payed_by_command_update_for_master(runner, pg):
    now = datetime.now(pytz.utc)
    offer_id = 209194477
    master_user_id = 29437831

    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers_reindex_master_user_id_and_payed_by.sql')
    await pg.execute(
        """
        INSERT INTO public.agents_hierarchy (
           id,
           row_version,
           realty_user_id,
           master_agent_user_id,
           created_at,
           updated_at
        )
        VALUES
           ($1, $2, $3, $4, $5, $6),
           ($7, $8, $9, $10, $11, $12)
        """,
        [
            1, 1, 1, master_user_id, now, now,
            2, 1, master_user_id, None, now, now,
        ]
    )

    await pg.execute(
        """
        INSERT INTO public.offers_billing_contracts (
           id,
           user_id,
           actor_user_id,
           publisher_user_id,
           offer_id,
           start_date,
           payed_till,
           row_version,
           is_deleted,
           created_at,
           updated_at
        )
        VALUES
           ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
        """,
        [
            1, 1, 1, master_user_id, offer_id, now, now, 1, False, now, now
        ]
    )

    await pg.execute(
        """
        INSERT INTO offers_reindex_queue(offer_id, created_at)
        VALUES
            ($1, current_timestamp)
        """,
        [offer_id]
    )

    # act
    await runner.start_background_python_command('reindex-offers-master-and-payed-by')
    await asyncio.sleep(2)

    # assert
    row = await pg.fetchrow('SELECT * FROM offers WHERE offer_id = $1', [offer_id])
    assert row['master_user_id'] == master_user_id
    assert row['old_master_user_id'] == master_user_id
    assert row['payed_by'] == master_user_id
