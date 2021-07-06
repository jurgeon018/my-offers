from pathlib import Path

import pytest


@pytest.fixture(autouse=True, scope='session')
async def start(runner, pg, queue_service, cassandra_service, global_runtime_settings, cassandra_statistics):
    await global_runtime_settings.set(
        RABBITMQ_CONNECT_TO_QUEUE_MASTER=False,
        RABBITMQ_CHECK_QUEUE_MASTER_INTERVAL=0,
    )

    await cassandra_statistics.execute_scripts(Path('contrib') / 'cassandra' / 'schema_for_tests.ddl')

    await cassandra_service.get_keyspace(alias='search_coverage', keyspace='search_coverage')

    await pg.execute_scripts((Path('contrib') / 'postgresql' / 'migrations').glob('*.sql'))

    await runner.start_background_python_command('process_announcement_consumer')
    await runner.start_background_python_command('save_announcement_contract_consumer')
    await runner.start_background_python_command('update_offer_duplicates_consumer')
    await runner.start_background_python_command('new_offer_duplicate_notification_consumer')
    await runner.start_background_python_command('offer_duplicate_price_changed_notification_consumer')
    await runner.start_background_python_command('process_announcement_from_elasticapi_consumer')
    await runner.start_background_python_command('save_announcement_contract_consumer')
    await runner.start_background_python_command('save_offer_relevance_warning_consumer')
    await runner.start_background_python_command('update_offer_master_user_consumer')

    await queue_service.wait_consumer('my-offers.process_announcement_from_elasticapi', timeout=300)


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
async def moderation_mock(http_mock_service):
    yield await http_mock_service.make_microservice_mock('moderation')


@pytest.fixture(scope='session')
async def search_offers_mock(http_mock_service):
    yield await http_mock_service.make_microservice_mock('search-offers')


@pytest.fixture(scope='session')
async def moderation_checks_orchestrator_mock(http_mock_service):
    yield await http_mock_service.make_microservice_mock('moderation-checks-orchestrator')


@pytest.fixture(scope='session')
async def price_estimator_mock(http_mock_service):
    yield await http_mock_service.make_microservice_mock('price-estimator')


@pytest.fixture(scope='session')
async def monolith_cian_announcementapi_mock(http_mock_service):
    yield await http_mock_service.make_microservice_mock('monolith_cian_announcementapi')


@pytest.fixture(scope='session')
async def monolith_cian_bill_mock(http_mock_service):
    yield await http_mock_service.make_microservice_mock('monolith-cian-bill')


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


@pytest.fixture(scope='session')
async def users_mock(http_mock_service):
    yield await http_mock_service.make_microservice_mock('users')


@pytest.fixture(scope='session')
async def favorites_mock(http_mock_service):
    yield await http_mock_service.make_microservice_mock('favorites')


@pytest.fixture(scope='session')
async def callbook_mock(http_mock_service):
    yield await http_mock_service.make_microservice_mock('callbook')


@pytest.fixture(scope='session')
async def cassandra_statistics(cassandra_service):
    yield await cassandra_service.get_keyspace(alias='statistics', keyspace='statistics')


@pytest.fixture(scope='session')
async def agents_mock(http_mock_service):
    yield await http_mock_service.make_microservice_mock('agents')


@pytest.fixture(scope='session')
async def monolith_python_mock(http_mock_service):
    yield await http_mock_service.make_microservice_mock('monolith-python')
