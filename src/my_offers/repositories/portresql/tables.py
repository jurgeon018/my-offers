from enum import Enum

import sqlalchemy as sa
from my_offers import enums
from sqlalchemy.dialects.postgresql import ENUM
from typing import List

_metadata = sa.MetaData()


def get_names(enum: Enum) -> List[str]:
    result = []
    for value in enum:
        result.append(value.name)

    return result


_deal_type = ENUM(*get_names(enums.DealType), name='deal_type', )
_offer_type = ENUM(*get_names(enums.OfferType), name='offer_type',)
_offer_status = ENUM(*get_names(enums.OfferStatus), name='offer_type',)
_service = ENUM(*get_names(enums.Service), name='service',)


offers = sa.Table(
    'offers',
    _metadata,
    sa.Column('offer_id', sa.BIGINT, primary_key=True),
    sa.Column('master_user_id', sa.BIGINT, nullable=False),
    sa.Column('user_id', sa.BIGINT, nullable=False),
    sa.Column('deal_type', _deal_type, nullable=False),
    sa.Column('offer_type', _offer_type, nullable=False),
    sa.Column('status', _offer_status, nullable=False),
    sa.Column('services', sa.ARRAY(_service), nullable=False),
    sa.Column('search_text', sa.TEXT, nullable=False),
    sa.Column('is_manual', sa.BOOLEAN, nullable=False),
    sa.Column('is_in_hidden_base', sa.BOOLEAN, nullable=False),
    sa.Column('has_photo', sa.BOOLEAN, nullable=False),
    sa.Column('row_version', sa.BIGINT, nullable=False),
    sa.Column('raw_data', sa.JSON, nullable=False),
    sa.Column('created_at', sa.TIMESTAMP, nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP, nullable=False),
)
