import json
from datetime import datetime
from typing import List, Tuple

import asyncpgsa
import pytz
from simple_settings import settings
from sqlalchemy.dialects.postgresql import insert

from my_offers import enums, pg
from my_offers.mappers.object_model import object_model_mapper
from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel
from my_offers.repositories.offers_duplicates.entities import Duplicate
from my_offers.repositories.postgresql import tables


async def update_offers_duplicates(duplicates: List[Duplicate]) -> None:
    now = datetime.now(tz=pytz.UTC)

    data = [
        {
            'offer_id': duplicate.offer_id,
            'group_id': duplicate.duplicate_group_id,
            'created_at': now,
        } for duplicate in duplicates
    ]

    insert_query = insert(tables.offers_duplicates)

    query, params = asyncpgsa.compile_query(
        insert_query
        .values(data)
        .on_conflict_do_nothing()
        # todo: добавить логику https://jira.cian.tech/browse/CD-80218
        # обновлять group_id
    )

    await pg.get().execute(query, *params)


async def get_offer_duplicates(offer_id: int, limit: int, offset: int) -> Tuple[List[ObjectModel], int]:
    query = """
    select
        o.raw_data,
        count(*) OVER () AS total_count
    from
        offers_duplicates od
        join offers o on o.offer_id = od.offer_id
    where
        od.group_id = (select group_id from offers_duplicates where offer_id = $1)
        and od.offer_id <> $2
        and o.status_tab = $3
    order by
        o.sort_date desc
    limit $4
    offset $5
    """

    result = await pg.get().fetch(
        query,
        offer_id,
        offer_id,
        enums.OfferStatusTab.active.value,
        limit,
        offset,
        timeout=settings.DB_TIMEOUT
    )

    if not result:
        return [], 0

    models = [object_model_mapper.map_from(json.loads(r['raw_data'])) for r in result]
    total = result[0]['total_count']

    return models, total
