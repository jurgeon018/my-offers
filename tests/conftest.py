import pytest
from cian_cache import cached
from cian_core.postgres import PostgresConnection
from cian_test_utils import future
from tornado import web

from my_offers import pg
from my_offers.web.urls import urlpatterns


@pytest.fixture
def app():
    return web.Application(urlpatterns)


@pytest.fixture(autouse=True)
def pg_connection(mocker):
    connection = mocker.Mock(spec=PostgresConnection)
    connection.execute.return_value = future()
    connection.fetch.return_value = future([])
    connection.fetchrow.return_value = future([])
    connection.fetchval.return_value = future(None)

    mocker.patch.object(pg, 'get', return_value=connection)

    return connection


async def cache_decorator(instance, f, options, *args, **kwargs):  # pylint: disable=unused-argument
    return await f(*args, **kwargs)


@pytest.fixture(autouse=True)
def cached_mock(mocker):
    return mocker.patch.object(cached, 'decorator', side_effect=cache_decorator)
