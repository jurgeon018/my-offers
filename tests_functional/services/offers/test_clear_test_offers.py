import asyncio
from pathlib import Path


async def test(runner, pg):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'clear_offers.sql')

    # act
    await runner.run_python_command('clear-test-offers-cron')
    await asyncio.sleep(2)

    rows = await pg.fetch('SELECT offer_id FROM offers_delete_queue')

    # assert
    assert len(rows) == 1
    assert rows[0]['offer_id'] == 2
