from enum import Enum, EnumMeta
from typing import List

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM

from my_offers import enums


_metadata = sa.MetaData()


def get_names(enum: EnumMeta) -> List[str]:
    result = []
    for value in enum:  # type: Enum
        result.append(value.name)

    return result


_deal_type = ENUM(*get_names(enums.DealType), name='deal_type')
_offer_type = ENUM(*get_names(enums.OfferType), name='offer_type',)
_offer_status_tab = ENUM(*get_names(enums.OfferStatusTab), name='offer_type',)
_service = ENUM(*get_names(enums.Services), name='service',)


offers = sa.Table(
    'offers',
    _metadata,
    sa.Column('offer_id', sa.BIGINT, primary_key=True),
    sa.Column('master_user_id', sa.BIGINT, nullable=False),
    sa.Column('user_id', sa.BIGINT, nullable=False),
    sa.Column('deal_type', _deal_type, nullable=False),
    sa.Column('offer_type', _offer_type, nullable=False),
    sa.Column('status_tab', _offer_status_tab, nullable=False),
    sa.Column('services', sa.ARRAY(_service), nullable=False),
    sa.Column('search_text', sa.TEXT, nullable=False),
    sa.Column('is_manual', sa.BOOLEAN, nullable=False),
    sa.Column('is_in_hidden_base', sa.BOOLEAN, nullable=False),
    sa.Column('has_photo', sa.BOOLEAN, nullable=False),
    sa.Column('row_version', sa.BIGINT, nullable=False),
    sa.Column('raw_data', sa.JSON, nullable=False),
    sa.Column('created_at', sa.TIMESTAMP, nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP, nullable=False),
    sa.Column('total_area', sa.FLOAT),
    sa.Column('price', sa.FLOAT),
    sa.Column('price_per_meter', sa.FLOAT),
    sa.Column('walking_time', sa.FLOAT),
    sa.Column('street_name', sa.String),
    sa.Column('sort_date', sa.TIMESTAMP),
    sa.Column('is_test', sa.BOOLEAN),
)
