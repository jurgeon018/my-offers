from cian_core.context.handlers import RequestContextHandler
from cian_core.web import base_urls
from cian_web import get_handler
from tornado.web import url

from my_offers.web import handlers


urlpatterns = base_urls.urlpatterns + [
    url(r'/public/v1/get-offers/$', handlers.GetOffersHandler),
    url(
        r'/v1/update-offer/',
        get_handler(
            service=offers.update_offer,
            method='POST',  # pragma: no mutate
            request_schema=entities.UpdateOfferRequest,
            base_handler_cls=RequestContextHandler,
        )
    ),
]
