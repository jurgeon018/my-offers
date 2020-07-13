# pylint: skip-file
"""

Code generated by cian-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client monolith-cian-announcementapi`

cian-codegen version: 1.4.1

"""
from cian_http.api_client import Api

from . import entities


_api = Api(microservice_name='monolith-cian-announcementapi')
announcements_actions_v1_change_owner = _api.make_client(
    path='/announcements-actions/v1/change-owner/',
    method='POST',
    handle_http_exceptions=True,
    request_schema=entities.ChangeOwnerRequest,
    response_schema=entities.ChangeOwnerResponse,
)
announcements_actions_v1_get_job_status = _api.make_client(
    path='/announcements-actions/v1/get-job-status/',
    method='GET',
    handle_http_exceptions=True,
    request_schema=entities.AnnouncementsActionsV1GetJobStatus,
    response_schema=entities.GetJobStatusResponse,
)
announcements_actions_v1_restore = _api.make_client(
    path='/announcements-actions/v1/restore/',
    method='POST',
    handle_http_exceptions=True,
    request_schema=entities.RestoreRequest,
    response_schema=entities.RestoreResponse,
)
v1_get_announcement = _api.make_client(
    path='/v1/get-announcement/',
    method='GET',
    handle_http_exceptions=True,
    request_schema=entities.V1GetAnnouncement,
    response_schema=entities.ObjectModel,
)
v2_announcements_archive = _api.make_client(
    path='/v2/announcements/archive/',
    method='POST',
    handle_http_exceptions=True,
    request_schema=entities.ArchiveAnnouncementV2Request,
)
