# pylint: skip-file
"""

Code generated by cian-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client monolith-cian-bill`

cian-codegen version: 1.9.0

"""
from cian_http.api_client import Api

from . import entities


_api = Api(microservice_name='monolith-cian-bill')
v1_tariffication_get_deactivated_additional_services = _api.make_client(
    path='/v1/tariffication/get-deactivated-additional-services/',
    method='GET',
    handle_http_exceptions=True,
    request_schema=entities.V1TarifficationGetDeactivatedAdditionalServices,
    response_schema=entities.GetDeactivatedAdditionalServicesResponse,
)
