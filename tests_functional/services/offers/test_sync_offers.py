from pathlib import Path

from cian_functional_test_utils.pytest_plugin import MockResponse


async def test_sync_offers_command(
        runner,
        monolith_cian_ms_announcements_mock,
        pg,
):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')

    await monolith_cian_ms_announcements_mock.add_stub(
        method='GET',
        path='/v2/get-changed-announcements-ids/',
        query={
            'rowVersion': 0,
            'top': 1000,
        },
        response=MockResponse(body={'announcements': [
            {
                'id': 1,
                'row_version': 1,
                'flags': 3,
                'status': 'Deleted',
            },
            {
                'id': 2,
                'row_version': 2,
                'flags': 10,
                'status': 'Published',
            },
            {
                'id': 3,
                'row_version': 31466774651,
                'flags': 0,
                'status': 'Deleted',
            }
        ]})
    )

    # act
    await runner.run_python_command('sync-offers-command')

    rows = await pg.fetch('select * from offers_row_versions')

    # assert
    assert len(rows) == 3


async def test_sync_offers_command__no_offers__return(
        runner,
        monolith_cian_ms_announcements_mock,
        pg,
):
    # arrange
    await monolith_cian_ms_announcements_mock.add_stub(
        method='GET',
        path='/v2/get-changed-announcements-ids/',
        query={
            'rowVersion': 0,
            'top': 1000,
        },
        response=MockResponse(body={'announcements': []})
    )

    # act
    await runner.run_python_command('sync-offers-command')

    rows = await pg.fetch('select * from offers_row_versions')

    # assert
    assert len(rows) == 0


async def test_sync_offers_command__resend_all_offers(
        runner,
        monolith_cian_ms_announcements_mock,
        monolith_cian_realty_mock,
        pg,
        runtime_settings,
):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')
    await runtime_settings.set({'SYNC_OFFERS_RESEND_ALL': True})

    await monolith_cian_realty_mock.add_stub(
        method='POST',
        path='/api/v1/resend-reporting-messages/resend-announcements/',
        response=MockResponse(body={
            'id': 1,
        })
    )

    await monolith_cian_realty_mock.add_stub(
        method='GET',
        path='/api/v1/resend-reporting-messages/get-job/',
        response=MockResponse(body={
            'state': 'finished',
        })
    )

    await monolith_cian_ms_announcements_mock.add_stub(
        method='GET',
        path='/v2/get-changed-announcements-ids/',
        query={
            'rowVersion': 0,
            'top': 1000,
        },
        response=MockResponse(body={'announcements': [
            {
                'id': 1,
                'row_version': 1,
                'flags': 3,
                'status': 'Deleted',
            },
            {
                'id': 2,
                'row_version': 2,
                'flags': 10,
                'status': 'Published',
            },
            {
                'id': 3,
                'row_version': 31466774651,
                'flags': 0,
                'status': 'Deleted',
            }
        ]})
    )

    # act
    await runner.run_python_command('sync-offers-command')

    rows = await pg.fetch('select * from offers_row_versions')

    # assert
    assert len(rows) == 3
