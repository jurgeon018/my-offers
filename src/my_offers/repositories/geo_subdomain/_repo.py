# pylint: skip-file
"""

Code generated by cian-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client geo-subdomain`

cian-codegen version: 1.4.1

"""
from cian_http.api_client import Api

from . import entities


_api = Api(microservice_name='geo-subdomain')
v1_get_subdomains = _api.make_client(
    path='/v1/get-subdomains/',
    method='GET',
    handle_http_exceptions=True,
    response_schema=entities.GetSubdomainsResponse,
)
