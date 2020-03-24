from typing import Any, Dict, List, Optional, Tuple

import asyncpgsa
from cian_json import json
from sqlalchemy import and_, func, over, select

from my_offers import pg
from my_offers.enums import GetOffersSortType
from my_offers.mappers.object_model import object_model_mapper
from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel
from my_offers.repositories.postgresql import tables
from my_offers.repositories.postgresql.offer_conditions import prepare_conditions


OFFER_TABLE = tables.offers.c

SORT_TYPE_MAP = {
    GetOffersSortType.by_default: OFFER_TABLE.sort_date.desc(),
    GetOffersSortType.by_price_min: OFFER_TABLE.price.desc(),
    GetOffersSortType.by_price_max: OFFER_TABLE.price,
    GetOffersSortType.by_price_for_meter: OFFER_TABLE.price_per_meter.desc(),
    GetOffersSortType.by_area_min: OFFER_TABLE.total_area.desc(),
    GetOffersSortType.by_area_max: OFFER_TABLE.total_area,
    GetOffersSortType.by_walk_time: OFFER_TABLE.walking_time,
    GetOffersSortType.by_street: OFFER_TABLE.street_name,
    GetOffersSortType.by_offer_id: OFFER_TABLE.offer_id,
}


async def get_object_model(filters: Dict[str, Any]) -> Optional[ObjectModel]:
    object_models, _ = await get_object_models(
        filters=filters,
        limit=1,
        offset=0,
        sort_type=GetOffersSortType.by_default,
    )

    if not object_models:
        return None

    return object_models[0]


async def get_object_models(
        *,
        filters: Dict[str, Any],
        limit: int,
        offset: int,
        sort_type: GetOffersSortType,
) -> Tuple[List[ObjectModel], int]:
    conditions = _prepare_conditions(filters)
    sort = _prepare_sort_order(sort_type)

    sql = (
        select([OFFER_TABLE.raw_data, over(func.count()).label('total_count')])
        .where(and_(*conditions))
        .order_by(*sort)
        .limit(limit)
        .offset(offset)
    )

    query, params = asyncpgsa.compile_query(sql)
    result = await pg.get().fetch(query, *params)

    if not result:
        return [], 0

    models = [object_model_mapper.map_from(json.loads(r['raw_data'])) for r in result]
    total = result[0]['total_count']

    return models, total


def _prepare_conditions(filters: Dict[str, Any]) -> List:
    conditions = prepare_conditions(filters)

    if services := filters.get('services'):
        conditions.append(OFFER_TABLE.services.overlap(services))
    if search_text := filters.get('search_text'):
        conditions.append(
            func.to_tsvector('russian', OFFER_TABLE.search_text).match(search_text, postgresql_regconfig='russian')
        )

    return conditions


def _prepare_sort_order(sort_type: GetOffersSortType):
    return [SORT_TYPE_MAP[sort_type].nullslast(), OFFER_TABLE.offer_id]


async def get_object_model_by_id(offer_id: int) -> Optional[ObjectModel]:
    query = 'SELECT raw_data FROM offers WHERE offer_id = $1'

    row = await pg.get().fetchrow(query, offer_id)

    if not row:
        return None

    return object_model_mapper.map_from(json.loads(row['raw_data']))
