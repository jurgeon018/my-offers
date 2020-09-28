from pathlib import Path

import pytest


@pytest.fixture(autouse=True, scope='session')
async def start(runner, pg, queue_service, cassandra_service, global_runtime_settings):
    await global_runtime_settings.set(
        RABBITMQ_CONNECT_TO_QUEUE_MASTER=False,
        RABBITMQ_CHECK_QUEUE_MASTER_INTERVAL=0,
    )

    await cassandra_service.get_keyspace(alias='statistics', keyspace='statistics')
    await cassandra_service.get_keyspace(alias='search_coverage', keyspace='search_coverage')

    await pg.execute_scripts((Path('contrib') / 'postgresql' / 'migrations').glob('*.sql'))

    await runner.start_background_python_command('process_announcement_consumer')
    await runner.start_background_python_command('update_offer_duplicates_consumer')
    await runner.start_background_python_command('new_offer_duplicate_notification_consumer')
    await runner.start_background_python_command('process_announcement_from_elasticapi_consumer')

    await queue_service.wait_consumer('my-offers.new_offer_duplicate_notification.SNACHEVA', timeout=30)
    await queue_service.wait_consumer('my-offers.process_announcement_from_elasticapi', timeout=30)


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


@pytest.fixture(scope='session')
async def price_estimator_mock(http_mock_service):
    yield await http_mock_service.make_microservice_mock('price-estimator')


@pytest.fixture(scope='session')
async def monolith_cian_announcementapi_mock(http_mock_service):
    yield await http_mock_service.make_microservice_mock('monolith_cian_announcementapi')


@pytest.fixture(scope='session')
async def monolith_cian_ms_announcements_mock(http_mock_service):
    yield await http_mock_service.make_microservice_mock('monolith-cian-ms-announcements')


@pytest.fixture(scope='session')
async def monolith_cian_elasticapi_mock(http_mock_service):
    yield await http_mock_service.make_microservice_mock('monolith-cian-elasticapi')


@pytest.fixture(scope='session')
async def monolith_cian_realty_mock(http_mock_service):
    yield await http_mock_service.make_microservice_mock('monolith-cian-realty')


@pytest.fixture(scope='session')
async def emails_mock(http_mock_service):
    yield await http_mock_service.make_microservice_mock('emails')
