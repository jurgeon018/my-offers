# pylint: skip-file
"""

Code generated by cian-codegen; DO NOT EDIT.

To re-generate, run `codegen generate-client monolith-cian-elasticapi`

cian-codegen version: 1.4.1

"""
from typing import List

from cian_http.api_client import Api

from . import entities


_api = Api(microservice_name='monolith-cian-elasticapi')
get_api_elastic_announcement_get = _api.make_client(
    path='/api/elastic/announcement/get/',
    method='GET',
    handle_http_exceptions=True,
    request_schema=entities.GetApiElasticAnnouncementGet,
    response_schema=entities.ElasticResultIElasticAnnouncementElasticAnnouncementError,
    default_timeout=5 # TODO: remove
)
post_api_elastic_announcement_get = _api.make_client(
    path='/api/elastic/announcement/get/',
    method='POST',
    handle_http_exceptions=True,
    request_schema=List[int],
    response_schema=entities.ElasticResultIElasticAnnouncementElasticAnnouncementError,
)
