from typing import Any, Dict, List

import sqlalchemy as sa
from sqlalchemy import any_, cast, func

from my_offers.repositories.postgresql import tables


OFFER_TABLE = tables.offers.c

FILTERS_MAP = {
    'status_tab': OFFER_TABLE.status_tab,
    'deal_type': OFFER_TABLE.deal_type,
    'offer_type': OFFER_TABLE.offer_type,
    'has_photo': OFFER_TABLE.has_photo,
    'is_manual': OFFER_TABLE.is_manual,
    'is_in_hidden_base': OFFER_TABLE.is_in_hidden_base,
    'master_user_id': OFFER_TABLE.master_user_id,
    'user_id': OFFER_TABLE.user_id,
    'sub_agent_ids': OFFER_TABLE.user_id,
    'offer_id': OFFER_TABLE.offer_id,
}


def prepare_conditions(filters: Dict[str, Any]) -> List:
    conditions = _prepare_basic_conditions(filters)

    if services := filters.get('services'):
        conditions.append(OFFER_TABLE.services.overlap(services))
    if search_text := filters.get('search_text'):
        tsquery = func.plainto_tsquery('russian', search_text)
        tsvector = func.to_tsvector('russian', OFFER_TABLE.search_text)
        conditions.append(tsvector.op('@@')(tsquery))

    return conditions


def _prepare_basic_conditions(filters: Dict[str, Any]) -> List:
    conditions = []
    for key, value in filters.items():
        if key not in FILTERS_MAP:
            continue
        if value is None:
            continue
        field = FILTERS_MAP[key]
        if isinstance(value, list):
            conditions.append(field == any_(cast(value, sa.ARRAY(field.type))))
        else:
            conditions.append(field == value)

    return conditions
