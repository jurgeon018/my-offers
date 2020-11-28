import asyncio


async def test_clean_users(runner, pg):
    # act
    await runner.run_python_command('clean-users-command')
    await asyncio.sleep(2)

    rows = await pg.fetch('select * from users_reindex_queue')

    # assert
    assert len(rows) == 0
