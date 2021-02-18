from typing import Any, Dict, List, Optional

import asyncpgsa
from cian_json import json
from simple_settings import settings
from sqlalchemy import and_, func, select

from my_offers import enums, pg
from my_offers.helpers.statsd import async_statsd_timer
from my_offers.mappers.object_model import object_model_mapper
from my_offers.repositories.monolith_cian_announcementapi.entities import ObjectModel
from my_offers.repositories.postgresql import tables
from my_offers.repositories.postgresql.offer_conditions import prepare_conditions


OFFER_TABLE = tables.offers.c

SORT_TYPE_MAP = {
    enums.GetOffersSortType.by_default: OFFER_TABLE.sort_date.desc(),
    enums.GetOffersSortType.by_price_min: OFFER_TABLE.price.desc(),
    enums.GetOffersSortType.by_price_max: OFFER_TABLE.price,
    enums.GetOffersSortType.by_price_for_meter: OFFER_TABLE.price_per_meter.desc(),
    enums.GetOffersSortType.by_area_min: OFFER_TABLE.total_area.desc(),
    enums.GetOffersSortType.by_area_max: OFFER_TABLE.total_area,
    enums.GetOffersSortType.by_walk_time: OFFER_TABLE.walking_time,
    enums.GetOffersSortType.by_street: OFFER_TABLE.street_name,
    enums.GetOffersSortType.by_offer_id: OFFER_TABLE.offer_id,
}

SORT_TYPE_MOBILE_MAP = {
    enums.MobOffersSortType.update_date: OFFER_TABLE.sort_date.desc(),
    enums.MobOffersSortType.move_to_archive_date: OFFER_TABLE.sort_date.desc(),
    enums.MobOffersSortType.price_asc: OFFER_TABLE.price,
    enums.MobOffersSortType.price_desc: OFFER_TABLE.price.desc(),
}


async def get_object_model(filters: Dict[str, Any]) -> Optional[ObjectModel]:
    object_models = await get_object_models(
        filters=filters,
        limit=1,
        offset=0,
        sort_type=enums.GetOffersSortType.by_default,
    )

    if not object_models:
        return None

    return object_models[0]


@async_statsd_timer('psql.get_object_models_total_count')
async def get_object_models_total_count(filters: Dict[str, Any]):
    conditions = prepare_conditions(filters)

    query, params = asyncpgsa.compile_query(select([func.count()]).where(and_(*conditions)))

    return await pg.get().fetchval(query, *params, timeout=settings.DB_SLOW_TIMEOUT)


@async_statsd_timer('psql.get_object_models')
async def get_object_models(
        *,
        filters: Dict[str, Any],
        limit: int,
        offset: int,
        sort_type: enums.GetOffersSortType,
) -> List[ObjectModel]:
    conditions = prepare_conditions(filters)
    sort = _prepare_sort_order(sort_type)

    sql = (
        select([OFFER_TABLE.raw_data])
        .where(and_(*conditions))
        .order_by(*sort)
        .limit(limit)
        .offset(offset)
    )

    query, params = asyncpgsa.compile_query(sql)
    result = await pg.get().fetch(query, *params, timeout=settings.DB_SLOW_TIMEOUT)

    if not result:
        return []

    models = [object_model_mapper.map_from(json.loads(r['raw_data'])) for r in result]

    return models


def _prepare_sort_order(sort_type: enums.GetOffersSortType):
    return [SORT_TYPE_MAP[sort_type].nullslast(), OFFER_TABLE.offer_id]


def _prepare_sort_mobile_order(sort_type: enums.MobOffersSortType):
    return [SORT_TYPE_MOBILE_MAP[sort_type].nullslast(), OFFER_TABLE.offer_id]


async def get_object_model_by_id(offer_id: int) -> Optional[ObjectModel]:
    query = 'SELECT raw_data FROM offers WHERE offer_id = $1'

    row = await pg.get().fetchrow(query, offer_id)

    if not row:
        return None

    return object_model_mapper.map_from(json.loads(row['raw_data']))


async def get_offers_by_ids(offer_ids: List[int]) -> List[ObjectModel]:
    query = """
    SELECT raw_data FROM offers WHERE offer_id = ANY($1::BIGINT[]) AND status_tab <> $2 ORDER BY sort_date DESC
    """

    rows = await pg.get().fetch(query, offer_ids, enums.OfferStatusTab.deleted.value)

    return [object_model_mapper.map_from(json.loads(r['raw_data'])) for r in rows]


async def get_offers_by_ids_keep_order(offer_ids: List[int]) -> List[ObjectModel]:
    query = """
    SELECT
        raw_data
    FROM
        offers
    WHERE
        offer_id = ANY($1::BIGINT[]) AND status_tab <> $2
    ORDER BY
        array_position($1::BIGINT[], offer_id)
    """

    rows = await pg.get().fetch(query, offer_ids, enums.OfferStatusTab.deleted.value)

    return [object_model_mapper.map_from(json.loads(r['raw_data'])) for r in rows]
