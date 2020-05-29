# pylint: skip-file
"""

Code generated by cian-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client notification-center`

cian-codegen version: 1.4.3

"""
from cian_http.api_client import Api

from . import entities


_api = Api(microservice_name='notification-center')
v2_register_notifications = _api.make_client(
    path='/v2/register-notifications/',
    method='POST',
    handle_http_exceptions=True,
    request_schema=entities.RegisterNotificationsV2Request,
)
