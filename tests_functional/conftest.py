import pytest
from pathlib import Path


@pytest.fixture(autouse=True, scope='session')
async def start(runner, pg):
    await pg.execute_scripts(Path('contrib') / 'schema.sql')
    await runner.start_background_python_web()


@pytest.fixture(name='pg', scope='session')
async def pg_fixture(postgres_service):
    yield await postgres_service.get_database_by_alias('my_offers')
