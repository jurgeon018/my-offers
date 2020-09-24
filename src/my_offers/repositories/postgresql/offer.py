from datetime import datetime
from typing import Any, Dict, List, Optional

import asyncpgsa
import pytz
from simple_settings import settings
from sqlalchemy import and_, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql.functions import count

from my_offers import entities, enums, pg
from my_offers.entities import OfferRowVersion
from my_offers.entities.get_offers import OfferCounters
from my_offers.entities.offer import ReindexOffer
from my_offers.enums import OfferPayedByType, OfferStatusTab
from my_offers.helpers.fields import get_offer_payed_by
from my_offers.helpers.statsd import async_statsd_timer
from my_offers.mappers.offer_mapper import (
    offer_mapper,
    offer_row_version_mapper,
    offers_creation_date_mapper,
    reindex_offer_mapper,
)
from my_offers.repositories.postgresql import tables
from my_offers.repositories.postgresql.offer_conditions import prepare_conditions


async def save_offer(offer: entities.Offer, event_date: datetime) -> None:
    """ Сохранить любое объявление, кроме архива. """
    insert_query = insert(tables.offers)

    now = datetime.now(tz=pytz.UTC)
    values = offer_mapper.map_to(offer)
    values['created_at'] = now
    values['updated_at'] = now
    values['event_date'] = event_date

    query, params = asyncpgsa.compile_query(
        insert_query
        .values([values])
        .on_conflict_do_update(
            index_elements=[tables.offers.c.offer_id],
            where=(
                tables.offers.c.row_version < offer.row_version
            ),
            set_={
                'master_user_id': insert_query.excluded.master_user_id,
                'user_id': insert_query.excluded.user_id,
                'deal_type': insert_query.excluded.deal_type,
                'offer_type': insert_query.excluded.offer_type,
                'status_tab': insert_query.excluded.status_tab,
                'services': insert_query.excluded.services,
                'is_manual': insert_query.excluded.is_manual,
                'is_in_hidden_base': insert_query.excluded.is_in_hidden_base,
                'has_photo': insert_query.excluded.has_photo,
                'search_text': insert_query.excluded.search_text,
                'price': insert_query.excluded.price,
                'price_per_meter': insert_query.excluded.price_per_meter,
                'total_area': insert_query.excluded.total_area,
                'street_name': insert_query.excluded.street_name,
                'walking_time': insert_query.excluded.walking_time,
                'sort_date': insert_query.excluded.sort_date,
                'raw_data': insert_query.excluded.raw_data,
                'row_version': insert_query.excluded.row_version,
                'is_test': insert_query.excluded.is_test,
                'updated_at': insert_query.excluded.updated_at,
                'event_date': insert_query.excluded.event_date,
            }
        )
    )

    await pg.get().execute(query, *params)


async def save_offer_archive(offer: entities.Offer, event_date: datetime) -> None:
    """ Сохранить архивное объявление.
        Если объявление уже есть в БД, то row_version не обновляем.

        Realty объявление, которое перенесли в архив чаще всего приходит с row_version = 1.
    """
    insert_query = insert(tables.offers)

    now = datetime.now(tz=pytz.UTC)
    values = offer_mapper.map_to(offer)
    values['created_at'] = now
    values['updated_at'] = now
    values['event_date'] = event_date

    query, params = asyncpgsa.compile_query(
        insert_query
        .values([values])
        .on_conflict_do_update(
            index_elements=[tables.offers.c.offer_id],
            where=(
                tables.offers.c.event_date < event_date
            ),
            set_={
                'master_user_id': insert_query.excluded.master_user_id,
                'user_id': insert_query.excluded.user_id,
                'deal_type': insert_query.excluded.deal_type,
                'offer_type': insert_query.excluded.offer_type,
                'status_tab': insert_query.excluded.status_tab,
                'services': insert_query.excluded.services,
                'is_manual': insert_query.excluded.is_manual,
                'is_in_hidden_base': insert_query.excluded.is_in_hidden_base,
                'has_photo': insert_query.excluded.has_photo,
                'search_text': insert_query.excluded.search_text,
                'price': insert_query.excluded.price,
                'price_per_meter': insert_query.excluded.price_per_meter,
                'total_area': insert_query.excluded.total_area,
                'street_name': insert_query.excluded.street_name,
                'walking_time': insert_query.excluded.walking_time,
                'sort_date': insert_query.excluded.sort_date,
                'raw_data': insert_query.excluded.raw_data,
                'is_test': insert_query.excluded.is_test,
                'updated_at': insert_query.excluded.updated_at,
                'event_date': event_date,
            }
        )
    )

    await pg.get().execute(query, *params)


async def update_offer(offer: entities.Offer):
    now = datetime.now(tz=pytz.UTC)
    values = offer_mapper.map_to(offer)
    values['updated_at'] = now

    query, params = asyncpgsa.compile_query(
        update(tables.offers)
        .values(values)
        .where(
            and_(
                tables.offers.c.offer_id == offer.offer_id,
                tables.offers.c.row_version <= offer.row_version,
            )
        )
    )

    await pg.get().execute(query, *params)


async def get_offer_by_id(offer_id: int) -> Optional[entities.Offer]:
    query = 'SELECT * FROM offers WHERE offer_id = $1'

    row = await pg.get().fetchrow(query, offer_id)

    if not row:
        return None

    return offer_mapper.map_from(row)


@async_statsd_timer('psql.get_offer_counters')
async def get_offer_counters(filters: Dict[str, Any]) -> OfferCounters:
    conditions = prepare_conditions(filters)
    status_tab = tables.offers.c.status_tab
    query, params = asyncpgsa.compile_query(
        select([status_tab, count().label('cnt')])
        .where(and_(*conditions))
        .group_by(status_tab)
    )

    rows = await pg.get().fetch(query, *params, timeout=settings.DB_TIMEOUT)
    counters = {row['status_tab']: row['cnt'] for row in rows}

    return OfferCounters(
        active=counters.get('active', 0),
        not_active=counters.get('notActive', 0),
        declined=counters.get('declined', 0),
        archived=counters.get('archived'),
    )


async def get_offers_for_reindex(offer_ids: List[int]) -> List[ReindexOffer]:
    query = 'SELECT offer_id, raw_data, updated_at FROM offers WHERE offer_id = ANY($1::BIGINT[])'

    rows = await pg.get().fetch(query, offer_ids)

    return [reindex_offer_mapper.map_from(row) for row in rows]


async def get_offers_id_older_than(
        *,
        date: datetime,
        status_tab: enums.OfferStatusTab,
        limit: int
) -> List[int]:
    query = """SELECT offer_id FROM offers where status_tab = $1 and updated_at <= $2 limit $3"""

    rows = await pg.get().fetch(
        query,
        status_tab.name,
        date,
        limit
    )
    offer_ids = [row['offer_id'] for row in rows]
    return offer_ids


async def get_offers_update_at(offer_ids: List[int]) -> Dict[int, datetime]:
    query = 'SELECT offer_id, updated_at FROM offers WHERE offer_id = ANY($1::BIGINT[])'

    rows = await pg.get().fetch(query, offer_ids, timeout=settings.DB_TIMEOUT)

    return {row['offer_id']: row['updated_at'] for row in rows}


async def get_offers_creation_date(master_user_id: int, offer_ids: List[int]) -> List[entities.OfferCreationDate]:
    query = """
    SELECT
        offer_id,
        raw_data->>'creationDate' as creation_date
    FROM
        offers
    WHERE
        master_user_id = $1
        AND offer_id = ANY($2::BIGINT[])
    """

    rows = await pg.get().fetch(query, master_user_id, offer_ids, timeout=settings.DB_TIMEOUT)

    return [offers_creation_date_mapper.map_from(row) for row in rows]


async def get_offers_row_version(offer_ids: List[int]) -> List[OfferRowVersion]:
    query = """
    SELECT
        offer_id,
        row_version
    FROM
        offers
    WHERE
        offer_id = ANY($1::BIGINT[])
    """

    rows = await pg.get().fetch(query, offer_ids)

    return [offer_row_version_mapper.map_from(row) for row in rows]


async def update_offer_master_user_id(*, offer_id: int, master_user_id: int) -> None:
    query = """
    update offers set master_user_id = $1 where offer_id = $2 and master_user_id <> $3
    """

    await pg.get().execute(query, master_user_id, offer_id, master_user_id)


@async_statsd_timer('psql.get_offers_ids_by_tab')
async def get_offers_ids_by_tab(filters: Dict[str, Any]) -> List[int]:
    conditions = prepare_conditions(filters)
    query, params = asyncpgsa.compile_query(
        select([tables.offers.c.offer_id])
        .where(and_(*conditions))
    )

    rows = await pg.get().fetch(query, *params, timeout=settings.DB_TIMEOUT)

    return [row['offer_id'] for row in rows]


async def set_offers_is_deleted(offers_ids: List[int]) -> None:
    now = datetime.now(tz=pytz.UTC)
    values = {
        'status_tab': OfferStatusTab.deleted.value,
        'updated_at': now
    }

    query, params = asyncpgsa.compile_query(
        update(
            tables.offers
        ).values(
            values
        ).where(
            and_(
                tables.offers.c.offer_id.in_(offers_ids)
            )
        )
    )

    await pg.get().execute(query, *params)


async def get_offers_payed_by(offer_ids: List[int]) -> Dict[int, Optional[OfferPayedByType]]:
    query = """
    select
        offer_id,
        master_user_id,
        user_id,
        payed_by
    from
        offers
    where
        offer_id = any($1::bigint[])
    """

    rows = await pg.get().fetch(query, offer_ids, timeout=settings.DB_TIMEOUT)

    return {row['offer_id']: get_offer_payed_by(row['master_user_id'],
                                                row['user_id'],
                                                row['payed_by']) for row in rows}


async def update_offers_master_user_id_and_payed_by(offer_ids: List[str]):
    query = """
        with cte1 as (
        select
            a.offer_id, b.master_agent_user_id
        from
            offers as a
        inner join
            agents_hierarchy as b on a.user_id = b.realty_user_id
        where
            a.offer_id = ANY($1::BIGINT[])
        ), cte2 as (
        select
            c.offer_id, first_value (publisher_user_id)
                        over (partition by offer_id order by row_version desc) as publisher_user_id
        from
            offers_billing_contracts as c
        where
            c.offer_id = ANY($1::BIGINT[])
        )

        update
            offers
        set
            old_master_user_id = master_user_id,
            master_user_id = COALESCE(cte1.master_agent_user_id, cte2.publisher_user_id),
            payed_by = cte2.publisher_user_id
        from
            cte1
        inner join
            cte2
        on
            cte1.offer_id = cte2.offer_id
        where
            offers.offer_id = cte1.offer_id
    """

    await pg.get().execute(query, offer_ids)
