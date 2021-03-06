# pylint: skip-file
"""

Code generated by cian-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client emails`

cian-codegen version: 1.4.1

"""
from cian_http.api_client import Api

from . import entities


_api = Api(microservice_name='emails')
emails_v2_send_email = _api.make_client(
    path='/emails/v2/send-email/',
    method='POST',
    handle_http_exceptions=True,
    request_schema=entities.SendEmailByEmailRequest,
    response_schema=entities.SendEmailByEmailResponse,
)
