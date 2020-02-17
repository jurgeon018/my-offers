import pytest
from cian_cache import cached
from tornado import web

from my_offers.web.urls import urlpatterns


@pytest.fixture
def app():
    return web.Application(urlpatterns)


async def cache_decorator(instance, f, options, *args, **kwargs):  # pylint: disable=unused-argument
    return await f(*args, **kwargs)


@pytest.fixture(autouse=True)
def cached_mock(mocker):
    return mocker.patch.object(cached, 'decorator', side_effect=cache_decorator)
