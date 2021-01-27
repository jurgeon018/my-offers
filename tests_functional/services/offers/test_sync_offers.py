from cian_functional_test_utils.pytest_plugin import MockResponse


async def test_sync_offers_command(
        runner,
        monolith_cian_elasticapi_mock,
        pg,
):
    # arrange
    await monolith_cian_elasticapi_mock.add_stub(
        method='GET',
        path='/api/elastic/announcement/v3/get-changed-ids/',
        query={
            'rowVersion': 0,
            'top': 10000,
        },
        response=MockResponse(body=[
            {
                'realty_object_id': 1,
                'row_version': 1,
            },
        ])
    )

    # act
    await runner.run_python_command('sync-offers-command')

    rows = await pg.fetch('select * from offers_row_versions')

    # assert
    assert len(rows) == 1


async def test_sync_offers_command__no_offers__return(
        runner,
        monolith_cian_elasticapi_mock,
        pg,
):
    # arrange
    await monolith_cian_elasticapi_mock.add_stub(
        method='GET',
        path='/api/elastic/announcement/v3/get-changed-ids/',
        query={
            'rowVersion': 0,
            'top': 10000,
        },
        response=MockResponse(body=[])
    )

    # act
    await runner.run_python_command('sync-offers-command')

    rows = await pg.fetch('select * from offers_row_versions')

    # assert
    assert len(rows) == 0
