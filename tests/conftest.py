import pytest
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
