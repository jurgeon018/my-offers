# pylint: skip-file
"""

Code generated by cian-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client price-estimator`

cian-codegen version: 1.4.3

"""
from cian_http.api_client import Api

from . import entities


_api = Api(microservice_name='price-estimator')
v1_get_estimation_for_realtors = _api.make_client(
    path='/v1/get-estimation-for-realtors/',
    method='POST',
    handle_http_exceptions=True,
    request_schema=entities.GetEstimationForRealtorsRequest,
    response_schema=entities.GetEstimationForRealtorsResponse,
)
