# pylint: skip-file
"""

Code generated by cian-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client moderation`

cian-codegen version: 1.9.0

"""
from cian_http.api_client import Api

from . import entities


_api = Api(microservice_name='moderation')
v1_get_image_offences_for_announcements = _api.make_client(
    path='/v1/get-image-offences-for-announcements/',
    method='POST',
    handle_http_exceptions=True,
    request_schema=entities.GetImageOffencesForAnnouncementsRequest,
    response_schema=entities.GetImageOffencesForAnnouncementsResponse,
)
v1_get_video_offences_for_announcements = _api.make_client(
    path='/v1/get-video-offences-for-announcements/',
    method='POST',
    handle_http_exceptions=True,
    request_schema=entities.GetVideoOffencesForAnnouncementsRequest,
    response_schema=entities.GetVideoOffencesForAnnouncementsResponse,
)
