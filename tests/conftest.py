import pytest
from tornado import web

from my_offers.web.urls import urlpatterns


@pytest.fixture
def app():
    return web.Application(urlpatterns)
