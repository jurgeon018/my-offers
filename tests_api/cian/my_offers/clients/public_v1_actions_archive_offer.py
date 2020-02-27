# pylint: skip-file
"""

Code generated by new-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client my-offers`

new-codegen version: 4.0.1

"""
from typing import Callable

from cian_automation.web import DecoratedBaseClient

from .. import entities


class PublicV1ActionsArchiveOffer(DecoratedBaseClient):
    _is_service = True
    microservice_name = 'my-offers'
    path = '/public/v1/actions/archive-offer/'
    path_args = []
    responses = {'post': entities.OfferActionResponse}
    request_post: Callable[..., 'entities.OfferActionResponse']
