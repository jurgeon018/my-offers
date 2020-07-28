import json
from datetime import datetime

import pytz
from cian_web.exceptions import BrokenRulesException, Error

from my_offers import entities
from my_offers.repositories.monolith_cian_announcementapi.entities import V1GetAnnouncement
from my_offers.repositories.monolith_cian_elasticapi import get_api_elastic_announcement_get
from my_offers.services.announcement import process_announcement


async def update_offer(request: entities.UpdateOfferRequest) -> None:
    try:
        response = await get_api_elastic_announcement_get(V1GetAnnouncement(id=request.offer_id))
    except Exception as e:
        raise BrokenRulesException([
            Error(
                message=str(e),
                code='error',
                key='offer_id'
            )
        ])
    if response.errors:
        raise BrokenRulesException([
            Error(
                message=response.errors[0].message,
                code='error',
                key='offer_id'
            )
        ])

    try:
        object_model = json.loads(response.success[0].offer_model)
        await process_announcement(object_model=object_model, event_date=datetime.now(pytz.UTC))
    except Exception as e:
        raise BrokenRulesException([
            Error(
                message=str(e),
                code='error',
                key='offer_id'
            )
        ])
