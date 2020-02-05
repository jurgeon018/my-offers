from cian_core.context.handlers import RequestContextHandler
from cian_core.web import base_urls
from cian_web import get_handler
from tornado.web import url

from my_offers import entities
from my_offers.services import offers


urlpatterns = base_urls.urlpatterns + [
    url(
        r'/v1/get-offers/$',
        get_handler(
            service=offers.get_offers,
            method='POST',  # pragma: no mutate
            request_schema=entities.GetOffersRequest,
            response_schema=entities.GetOffersResponse,
            base_handler_cls=RequestContextHandler,
        )
    ),
]
