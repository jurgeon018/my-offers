import json
from datetime import datetime

import pytz
from cian_web.exceptions import BrokenRulesException, Error

from my_offers import entities
from my_offers.mappers.object_model import object_model_mapper
from my_offers.repositories.monolith_cian_announcementapi.entities import V1GetAnnouncement
from my_offers.repositories.monolith_cian_elasticapi import get_api_elastic_announcement_get
from my_offers.repositories.monolith_cian_elasticapi.entities import (
    ElasticResultIElasticAnnouncementElasticAnnouncementError,
    GetApiElasticAnnouncementGet,
)
from my_offers.services.announcement import process_announcement


async def update_offer(request: entities.UpdateOfferRequest) -> None:
    try:
        response: ElasticResultIElasticAnnouncementElasticAnnouncementError = await get_api_elastic_announcement_get(
            GetApiElasticAnnouncementGet(ids=[request.offer_id])
        )
    except Exception as e:
        raise BrokenRulesException([
            Error(
                message=str(e),
                code='api_error',
                key='offer_id'
            )
        ])
    if response.errors:
        raise BrokenRulesException([
            Error(
                message=response.errors[0].message,
                code='response_error',
                key='offer_id'
            )
        ])

    try:
        object_model = object_model_mapper.map_from(json.loads(response.success[0].object_model))
        await process_announcement(object_model=object_model, event_date=datetime.now(pytz.UTC))
    except Exception as e:
        raise BrokenRulesException([
            Error(
                message=str(e),
                code='process_error',
                key='offer_id'
            )
        ])
