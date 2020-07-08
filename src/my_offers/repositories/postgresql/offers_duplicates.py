import json
from datetime import datetime
from typing import List, Tuple

import asyncpgsa
import pytz
import sqlalchemy as sa
from simple_settings import settings
from sqlalchemy.dialects.postgresql import insert

from my_offers import entities, enums, pg
from my_offers.enums import DealType, OfferType
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


async def get_offer_duplicates_count(offer_id: int) -> int:
    query = """
    select
        count(*) as cnt
    from
        offers_duplicates od
        join offers o on o.offer_id = od.offer_id
    where
        od.group_id = (select group_id from offers_duplicates where offer_id = $1)
        and od.offer_id <> $2
        and o.status_tab = $3;
    """
    row = await pg.get().fetchrow(
        query,
        offer_id,
        offer_id,
        enums.OfferStatusTab.active.value
    )
    return row['cnt']


async def delete_offers_duplicates(offer_ids: List[int]) -> None:
    query = 'DELETE FROM offers_duplicates WHERE offer_id = ANY($1::BIGINT[])'

    await pg.get().execute(query, offer_ids)


async def get_offers_duplicates_count(offer_ids: List[int]) -> List[entities.OfferDuplicatesCount]:
    query = """
    select
        d1.offer_id,
        count(*) - 1 as cnt
    from
        offers_duplicates d1
        join offers_duplicates d2 on d2.group_id = d1.group_id
        join offers o on o.offer_id = d2.offer_id
    where
        o.status_tab = 'active'
        and d1.offer_id = any($1::bigint[])
    group by
        d1.offer_id
    having
        count(*) > 1
    """

    rows = await pg.get().fetch(query, offer_ids)

    return [
        entities.OfferDuplicatesCount(
            offer_id=row['offer_id'],
            competitors_count=0,
            duplicates_count=row['cnt']
        )
        for row in rows
    ]


async def get_offer_duplicates_ids(offer_id: int) -> List[int]:
    query = """
    select
        offer_id
    from
        offers_duplicates
    where
        group_id = (select group_id from offers_duplicates where offer_id = $1);
    """
    result = await pg.get().fetch(query, offer_id, timeout=settings.DB_TIMEOUT)
    return [r['offer_id'] for r in result]


async def get_offers_in_same_building(
        *,
        deal_type: DealType,
        house_id: int,
        rooms_counts: Tuple[str, str, str],
        low_price: float,
        high_price: float,
        duplicates_ids: List[int],
        is_test: bool,
        limit: int,
        offset: int
) -> Tuple[List[ObjectModel], int]:
    query = """
    SELECT
        o.raw_data,
        count(*) OVER () AS total_count
    from
        offers o
    where
        o.house_id = $1
        and o.offer_type = $2
        and o.deal_type = $3
        and o.raw_data -> 'roomsCount' = any($4)
        and o.price >= $5
        and o.price  <= $6
        and o.offer_id <> all ($7::bigint[])
        and o.status_tab = $8
        and o.is_test = $9
    order by
        o.sort_date desc
    limit $10
    offset $11;
    """

    result = await pg.get().fetch(
        query,
        house_id,
        OfferType.flat.value,
        deal_type.value,
        rooms_counts,
        low_price,
        high_price,
        duplicates_ids,
        enums.OfferStatusTab.active.value,
        is_test,
        limit,
        offset,
        timeout=settings.DB_TIMEOUT
    )

    if not result:
        return [], 0

    models = [object_model_mapper.map_from(json.loads(r['raw_data'])) for r in result]
    total = result[0]['total_count']

    return models, total


async def get_similar_offers(
        *,
        deal_type: DealType,
        district_id: int,
        house_id: int,
        rooms_counts: Tuple[str, str, str],
        low_price: float,
        high_price: float,
        is_test: bool,
        offer_id: int,
        limit: int,
        offset: int
) -> Tuple[List[ObjectModel], int]:
    query = """
    SELECT
        o.raw_data,
        count(*) OVER () AS total_count
    from
        offers o
    where
        o.district_id = $1
        and (house_id != $2 or house_id is null)
        and o.offer_type = $3
        and o.deal_type = $4
        and o.raw_data -> 'roomsCount' = any($5)
        and o.price >= $6
        and o.price  <= $7
        and o.status_tab = $8
        and o.is_test = $9
        and o.offer_id <> $10
    order by
        o.sort_date desc
    limit $11
    offset $12;
    """

    result = await pg.get().fetch(
        query,
        district_id,
        house_id,
        OfferType.flat.value,
        deal_type.value,
        rooms_counts,
        low_price,
        high_price,
        enums.OfferStatusTab.active.value,
        is_test,
        offer_id,
        limit,
        offset,
        timeout=settings.DB_TIMEOUT
    )

    if not result:
        return [], 0

    models = [object_model_mapper.map_from(json.loads(r['raw_data'])) for r in result]
    total = result[0]['total_count']

    return models, total
