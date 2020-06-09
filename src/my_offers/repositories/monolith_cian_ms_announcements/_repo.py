# pylint: skip-file
"""

Code generated by cian-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client monolith-cian-ms-announcements`

cian-codegen version: 1.4.1

"""
from typing import List

from cian_http.api_client import Api

from . import entities


_api = Api(microservice_name='monolith-cian-ms-announcements')
v1_can_update_editdate = _api.make_client(
    path='/v1/can-update-editdate/',
    method='GET',
    handle_http_exceptions=True,
    request_schema=entities.V1CanUpdateEditdate,
    response_schema=List[entities.CanUpdateEditdateResult],
)
v1_get_changed_announcements_ids = _api.make_client(
    path='/v1/get-changed-announcements-ids/',
    method='GET',
    handle_http_exceptions=True,
    request_schema=entities.V1GetChangedAnnouncementsIds,
    response_schema=entities.GetChangedIdsResponse,
    default_timeout=60
)
v1_update_editdate = _api.make_client(
    path='/v1/update-editdate/',
    method='POST',
    handle_http_exceptions=True,
    request_schema=entities.UpdateEditdateRequest,
    response_schema=List[entities.UpdateEditdateResult],
)
