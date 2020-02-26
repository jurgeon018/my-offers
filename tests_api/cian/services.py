"""

Code generated by new-codegen; DO NOT EDIT.

To re-generate, run `new-codegen generate-client <microservice_name>`

new-codegen version: 4.0.1

"""
from cian_automation.context import LazyImport

from .announcementapi.api import Announcementapi
from .my_offers.api import MyOffers
from .qa_cian_proxy.api import QaCianProxy


class CianServices(metaclass=LazyImport):
    announcementapi: Announcementapi
    my_offers: MyOffers
    qa_cian_proxy: QaCianProxy
