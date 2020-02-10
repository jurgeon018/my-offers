from cian_core.web import base_urls
from tornado.web import url

from my_offers.web import handlers


urlpatterns = base_urls.urlpatterns + [
    url(r'/public/v1/get-offers/$', handlers.GetOffersHandler),
]
