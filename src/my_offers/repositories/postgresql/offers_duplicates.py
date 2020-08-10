import json
from datetime import datetime
from typing import List, Optional, Tuple

import asyncpgsa
import pytz
import sqlalchemy as sa
from simple_settings import settings
from sqlalchemy.dialects.postgresql import insert

from my_offers import entities, enums, pg
from my_offers.enums import DealType, DuplicateType, OfferType
from my_offers.mappers.object_model import object_model_mapper
from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel
from my_offers.repositories.offers_duplicates.entities import Duplicate
from my_offers.repositories.postgresql.tables import metadata


offers_duplicates = sa.Table(
    'offers_duplicates',
    metadata,
    sa.Column('offer_id', sa.BIGINT, primary_key=True),
    sa.Column('group_id', sa.BIGINT, nullable=False),
    sa.Column('created_at', sa.TIMESTAMP, nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP, nullable=True),
)


async def update_offers_duplicates(duplicates: List[Duplicate]) -> List[int]:
    now = datetime.now(tz=pytz.UTC)

    data = [
        {
            'offer_id': duplicate.offer_id,
            'group_id': duplicate.duplicate_group_id,
            'created_at': now,
        } for duplicate in duplicates
    ]

    insert_query = insert(offers_duplicates)

    query, params = asyncpgsa.compile_query(
        insert_query
        .values(data)
        .on_conflict_do_update(
            index_elements=[offers_duplicates.c.offer_id],
            set_={
                'group_id': insert_query.excluded.group_id,
                'updated_at': insert_query.excluded.created_at,
            }
        ).returning(
            offers_duplicates.c.offer_id,
            offers_duplicates.c.updated_at,
        )
    )

    rows = await pg.get().fetch(query, *params)
    if not rows:
        return []

    return [row['offer_id'] for row in rows if row['updated_at'] is None]


async def get_offer_duplicates(
        *,
        offer_id: int,
        limit: int,
        offset: int
) -> List[Tuple[ObjectModel, DuplicateType]]:
    query = """
    select
        o.raw_data
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
    offers_info: List[Tuple[ObjectModel, DuplicateType]] = []
    if not result:
        return offers_info
    for r in result:
        offers_info.append(
            (
                object_model_mapper.map_from(json.loads(r['raw_data'])),
                DuplicateType.duplicate
            )
        )
    return offers_info


async def get_duplicate_group_id(offer_id: int) -> Optional[int]:
    query = 'select group_id from offers_duplicates where offer_id = $1'
    row = await pg.get().fetchrow(query, offer_id)

    return row['group_id'] if row else None
