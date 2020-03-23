from typing import Any, Dict, List

import sqlalchemy as sa
from sqlalchemy import any_, cast

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
