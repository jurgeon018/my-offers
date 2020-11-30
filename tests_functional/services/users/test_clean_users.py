import asyncio

from cian_functional_test_utils.pytest_plugin import MockResponse


async def test_clean_users(runner, pg, users_mock):
    # arrange
    await pg.execute('insert into users_reindex_queue(user_id) values (1), (2)')

    await users_mock.add_stub(
        method='POST',
        path='/v1/get-users/',
        response=MockResponse(body={
            'users': [
                {'id': 1}
            ]
        })
    )

    # act
    await runner.run_python_command('clean-users-command')
    await asyncio.sleep(2)

    rows = await pg.fetch('select * from users_reindex_queue')

    # assert
    assert len(rows) == 0
