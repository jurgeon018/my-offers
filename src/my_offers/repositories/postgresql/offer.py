from datetime import datetime
from typing import Any, Dict, List, Optional
import copy
from typing import List, Optional
from datetime import datetime, timedelta

import asyncpgsa
import pytz
from sqlalchemy import and_, select, update
from simple_settings import settings
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql.functions import count

from my_offers import entities, enums, pg
from my_offers.entities.get_offers import OfferCounters
from my_offers.entities.offer import ReindexOffer
from my_offers.mappers.offer_mapper import offer_mapper, reindex_offer_mapper
from my_offers.repositories.postgresql import tables
from my_offers.repositories.postgresql.offer_conditions import prepare_conditions


async def save_offer(offer: entities.Offer) -> None:
    insert_query = insert(tables.offers)

    now = datetime.now(tz=pytz.UTC)
    values = offer_mapper.map_to(offer)
    values['created_at'] = now
    values['updated_at'] = now

    query, params = asyncpgsa.compile_query(
        insert_query
        .values([values])
        .on_conflict_do_update(
            index_elements=[tables.offers.c.offer_id],
            where=tables.offers.c.row_version < offer.row_version,
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


async def get_offer_counters(filters: Dict[str, Any]) -> OfferCounters:
    conditions = prepare_conditions(filters)
    status_tab = tables.offers.c.status_tab
    query, params = asyncpgsa.compile_query(
        select([status_tab, count().label('cnt')])
        .where(and_(*conditions))
        .group_by(status_tab)
    )

    rows = await pg.get().fetch(query, *params)
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


async def delete_offers_older_than(days_count: int = settings.COUNT_DAYS_HOLD_DELETED_OFFERS):
    need_date = datetime.now(tz=pytz.UTC) - timedelta(days=days_count)
    query = """DELETE FROM offers where status_tab = $1 and updated_at <= $2"""

    await pg.get().execute(
        query,
        enums.OfferStatusTab.deleted.name,
        need_date
    )
