from pathlib import Path

import pytest


@pytest.fixture(autouse=True, scope='session')
async def start(runner, pg, queue_service, cassandra_service):
    await cassandra_service.get_keyspace(alias='statistics', keyspace='statistics')
    await cassandra_service.get_keyspace(alias='search_coverage', keyspace='search_coverage')

    await pg.execute_scripts((Path('contrib') / 'postgresql' / 'migrations').glob('*.sql'))
    await runner.start_background_python_web()
    await runner.start_background_python_command('process_announcement_consumer')
    await runner.start_background_python_command('update_offer_duplicates_consumer')


@pytest.fixture(name='pg', scope='session')
async def pg_fixture(postgres_service):
    yield await postgres_service.get_database_by_alias('my_offers')


@pytest.fixture(scope='session')
async def offers_duplicates_mock(http_mock_service):
    yield await http_mock_service.make_microservice_mock('offers-duplicates')


@pytest.fixture(scope='session')
async def auction_mock(http_mock_service):
    yield await http_mock_service.make_microservice_mock('auction')


@pytest.fixture(scope='session')
async def notification_center_mock(http_mock_service):
    yield await http_mock_service.make_microservice_mock('notification-center')
