from typing import Dict, List, Optional

import asyncpgsa
import sqlalchemy as sa
from sqlalchemy import update
from sqlalchemy.dialects.postgresql import insert

from my_offers import entities, enums, pg
from my_offers.mappers.offer_mapper import offer_similar_mapper
from my_offers.repositories.postgresql.tables import deal_type, metadata


offers_similars_flat = sa.Table(
    'offers_similars_flat',
    metadata,
    sa.Column('offer_id', sa.BIGINT, primary_key=True),
    sa.Column('deal_type', deal_type, nullable=False),
    sa.Column('group_id', sa.BIGINT, nullable=True),
    sa.Column('house_id', sa.INT, nullable=True),
    sa.Column('district_id', sa.INT, nullable=True),
    sa.Column('price', sa.FLOAT, nullable=True),
    sa.Column('rooms_count', sa.INT, nullable=True),
    sa.Column('sort_date', sa.TIMESTAMP, nullable=False),
    sa.Column('old_price', sa.FLOAT, nullable=True),
)

offers_similars_test = sa.Table(
    'offers_similars_test',
    metadata,
    sa.Column('offer_id', sa.BIGINT, primary_key=True),
    sa.Column('deal_type', deal_type, nullable=False),
    sa.Column('group_id', sa.BIGINT, nullable=True),
    sa.Column('house_id', sa.INT, nullable=True),
    sa.Column('district_id', sa.INT, nullable=True),
    sa.Column('price', sa.FLOAT, nullable=True),
    sa.Column('rooms_count', sa.INT, nullable=True),
    sa.Column('sort_date', sa.TIMESTAMP, nullable=False),
    sa.Column('old_price', sa.FLOAT, nullable=True),
)

TABLES_MAP = {
    'flat': offers_similars_flat,
    'test': offers_similars_test,
}


async def get_offer_similar_for_update(*, suffix: str, offer_id: int) -> Optional[entities.OfferSimilar]:
    table_name = f'offers_similars_{suffix}'

    query = f'select * from {table_name} where offer_id = $1 for update'
    row = await pg.get().fetchrow(query, offer_id)

    return offer_similar_mapper.map_from(row) if row else None


async def insert_similar(*, suffix: str, similar: entities.OfferSimilar) -> None:
    table = TABLES_MAP[suffix]
    values = offer_similar_mapper.map_to(similar)
    query, params = asyncpgsa.compile_query(
        insert(table)
        .values([values])
    )
    await pg.get().execute(query, *params)


async def update_similar(*, suffix: str, similar: entities.OfferSimilar) -> None:
    table = TABLES_MAP[suffix]
    values = offer_similar_mapper.map_to(similar)
    query, params = asyncpgsa.compile_query(
        update(table)
        .where(table.c.offer_id == similar.offer_id)
        .values(values)
    )
    await pg.get().execute(query, *params)


async def delete(*, suffix: str, offer_id: int) -> None:
    table = TABLES_MAP[suffix]
    query, params = asyncpgsa.compile_query(
        sa.delete(table).where(table.c.offer_id == offer_id)
    )

    await pg.get().execute(query, *params)


async def update_group_id(offer_ids: List[int]) -> None:
    query = """
        update
            offers_similars_flat as os
        set
            group_id = od.group_id
        from
            offers_duplicates as od
        where
            od.offer_id = os.offer_id
            and od.offer_id = ANY($1::BIGINT[])
    """

    await pg.get().execute(query, offer_ids)


async def unset_group_id(offer_ids: List[int]) -> None:
    query = 'update offers_similars_flat set group_id = null where offer_id = ANY($1::BIGINT[])'

    await pg.get().execute(query, offer_ids)


async def get_similars_by_offer_id(
        *,
        offer_id: int,
        price_kf: float,
        room_delta: int,
        limit: int,
        offset: int,
        tab_type: enums.DuplicateTabType,
        suffix: str,
) -> Dict[int, enums.DuplicateType]:
    table = TABLES_MAP[suffix]
    tab_condition = _prepare_tab_condition(
        price_kf=price_kf,
        room_delta=room_delta,
        tab_type=tab_type
    )

    query = f"""
    with offer as (
        select
           offer_id,
           deal_type,
           group_id,
           house_id,
           district_id,
           price,
           rooms_count
        from
           {table}
        where
           offer_id = $1
    )
    select
       os.offer_id,
       case
         when os.group_id = offer.group_id then 'duplicate'
         when os.house_id = offer.house_id then 'sameBuilding'
         else 'similar'
       end as type
    from
      offer,
      {table} os
    where
      os.deal_type = offer.deal_type
      and os.offer_id <> offer.offer_id
      and ({tab_condition})
    order by
        case
           when os.group_id = offer.group_id then 1
           when os.house_id = offer.house_id then 2
           else 3
       end,
       os.sort_date desc
    limit $2
    offset $3
    """

    rows = await pg.get().fetch(query, offer_id, limit, offset)

    return {row['offer_id']: enums.DuplicateTabType(row['type']) for row in rows}


async def get_similars_counters_by_offer_ids(
        *,
        offer_ids: List[int],
        price_kf: float,
        room_delta: int,
        suffix: str,
        tab_type=enums.DuplicateTabType.all,
) -> List[entities.OfferSimilarCounter]:
    table = TABLES_MAP[suffix]
    tab_condition = _prepare_tab_condition(
        price_kf=price_kf,
        room_delta=room_delta,
        tab_type=tab_type,
    )

    query = f"""
    with offer as (
        select
           offer_id,
           deal_type,
           group_id,
           house_id,
           district_id,
           price,
           rooms_count
        from
           {table}
        where
           offer_id = any($1::bigint[])
    )
    select
       offer.offer_id,
       count(*) as total_count,
       sum(case when os.group_id = offer.group_id then 1 else 0 end) as duplicate_count,
       sum(
        case when (os.group_id <> offer.group_id or offer.group_id is null or os.group_id is null)
            and os.house_id = offer.house_id then 1 else 0 end) as house_count
    from
      offer,
      {table} os
    where
      os.deal_type = offer.deal_type
      and os.offer_id <> offer.offer_id
      and ({tab_condition})
    group by
        offer.offer_id
    """

    rows = await pg.get().fetch(query, offer_ids)

    return [_map_offer_similar_counter(row) for row in rows]


async def get_similar_counter_by_offer_id(
        *,
        offer_id: int,
        price_kf: float,
        room_delta: int,
        suffix: str,
) -> entities.OfferSimilarCounter:
    data = await get_similars_counters_by_offer_ids(
        offer_ids=[offer_id],
        price_kf=price_kf,
        room_delta=room_delta,
        suffix=suffix,
    )

    return data[0] if data else entities.OfferSimilarCounter(
        offer_id=offer_id,
        same_building_count=0,
        similar_count=0,
        duplicates_count=0,
        total_count=0,
    )


def _map_offer_similar_counter(row: Dict[str, int]) -> entities.OfferSimilarCounter:
    duplicates_count = row['duplicate_count']
    same_building_count = row['house_count']

    return entities.OfferSimilarCounter(
        offer_id=row['offer_id'],
        same_building_count=same_building_count,
        similar_count=row['total_count'] - duplicates_count - same_building_count,
        duplicates_count=duplicates_count,
        total_count=row['total_count'],
    )


def _prepare_tab_condition(
        *,
        tab_type: enums.DuplicateTabType,
        price_kf: float,
        room_delta: int,
) -> str:
    if tab_type.is_duplicate:
        tab_condition = 'os.group_id = offer.group_id'
    elif tab_type.is_same_building:
        tab_condition = f"""
            (os.group_id <> offer.group_id or offer.group_id is null or os.group_id is null)
            and os.house_id = offer.house_id
            and os.price >= offer.price * (1 - {price_kf})
            and os.price <= offer.price * (1 + {price_kf})
            and os.rooms_count >= offer.rooms_count - {room_delta}
            and os.rooms_count <= offer.rooms_count + {room_delta}
        """
    elif tab_type.is_similar:
        tab_condition = f"""
            (os.group_id <> offer.group_id or offer.group_id is null or os.group_id is null)
            and (os.house_id <> offer.house_id or offer.house_id is null or os.house_id is null)
            and os.district_id = offer.district_id
            and os.price >= offer.price * (1 - {price_kf})
            and os.price <= offer.price * (1 + {price_kf})
            and os.rooms_count >= offer.rooms_count - {room_delta}
            and os.rooms_count <= offer.rooms_count + {room_delta}
        """
    else:  # tab_type.is_all:
        tab_condition = f"""
            os.group_id = offer.group_id
            or (
                (
                    os.house_id = offer.house_id
                    or os.district_id = offer.district_id
                )
                and os.price >= offer.price * (1 - {price_kf})
                and os.price <= offer.price * (1 + {price_kf})
                and os.rooms_count >= offer.rooms_count - {room_delta}
                and os.rooms_count <= offer.rooms_count + {room_delta}
            )
        """

    return tab_condition


async def get_offer_similar(offer_id: int, suffix: str = 'flat') -> Optional[entities.OfferSimilar]:
    table_name = f'offers_similars_{suffix}'
    query = f'select * from {table_name} where offer_id = $1'
    row = await pg.get().fetchrow(query, offer_id)

    return offer_similar_mapper.map_from(row) if row else None


async def get_offers_similars_by_group_id(group_id: int) -> List[entities.OfferSimilar]:
    query = 'select * from offers_similars_flat where group_id = $1'
    rows = await pg.get().fetch(query, group_id)

    return [offer_similar_mapper.map_from(row) for row in rows]
