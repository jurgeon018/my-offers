from enum import Enum, EnumMeta
from typing import List

import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as psa

from my_offers import enums
from my_offers.repositories.monolith_cian_announcementapi.entities.publish_term import Services


metadata = sa.MetaData()


def get_names(enum: EnumMeta) -> List[str]:
    result = []
    for value in enum:  # type: Enum
        result.append(value.name)

    return result


_deal_type = psa.ENUM(*get_names(enums.DealType), name='deal_type')
_offer_type = psa.ENUM(*get_names(enums.OfferType), name='offer_type', )
_offer_status_tab = psa.ENUM(*get_names(enums.OfferStatusTab), name='offer_type', )
_service = psa.ENUM(*get_names(Services), name='offer_service', )

offers = sa.Table(
    'offers',
    metadata,
    sa.Column('offer_id', sa.BIGINT, primary_key=True),
    sa.Column('master_user_id', sa.BIGINT, nullable=False),
    sa.Column('user_id', sa.BIGINT, nullable=False),
    sa.Column('deal_type', _deal_type, nullable=False),
    sa.Column('offer_type', _offer_type, nullable=False),
    sa.Column('status_tab', _offer_status_tab, nullable=False),
    sa.Column('services', psa.ARRAY(_service), nullable=False),
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

offers_billing_contracts = sa.Table(
    'offers_billing_contracts',
    metadata,
    sa.Column('id', sa.BIGINT, primary_key=True),
    sa.Column('user_id', sa.BIGINT, nullable=False),
    sa.Column('actor_user_id', sa.BIGINT, nullable=False),
    sa.Column('publisher_user_id', sa.BIGINT, nullable=False),
    sa.Column('offer_id', sa.BIGINT, nullable=False),
    sa.Column('start_date', sa.TIMESTAMP, nullable=False),
    sa.Column('payed_till', sa.TIMESTAMP, nullable=False),
    sa.Column('row_version', sa.BIGINT, nullable=False),
    sa.Column('is_deleted', sa.BOOLEAN, nullable=False),
    sa.Column('created_at', sa.TIMESTAMP, nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP, nullable=False),
)

offers_last_import_error = sa.Table(
    'offers_last_import_error',
    metadata,
    sa.Column('offer_id', sa.BIGINT, primary_key=True),
    sa.Column('type', sa.String),
    sa.Column('message', sa.String),
    sa.Column('created_at', sa.TIMESTAMP, nullable=False),
)

_offence_status = psa.ENUM(*get_names(enums.ModerationOffenceStatus), name='offence_status')
offers_offences = sa.Table(
    'offers_offences',
    metadata,
    sa.Column('offence_id', sa.BIGINT, primary_key=True),
    sa.Column('offence_type', sa.BIGINT, nullable=False),
    sa.Column('offence_text', sa.TEXT, nullable=False),
    sa.Column('offence_status', _offence_status, nullable=False),
    sa.Column('offer_id', sa.BIGINT, nullable=False),
    sa.Column('row_version', sa.BIGINT, nullable=False),
    sa.Column('created_by', sa.BIGINT, nullable=False),
    sa.Column('created_date', sa.TIMESTAMP, nullable=False),
    sa.Column('created_at', sa.TIMESTAMP, nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP, nullable=False),
)

_account_type = psa.ENUM(*get_names(enums.AgentAccountType), name='account_type')
agents_hierarchy = sa.Table(
    'agents_hierarchy',
    metadata,
    sa.Column('id', sa.BIGINT, primary_key=True),
    sa.Column('account_type', _account_type, nullable=False),
    sa.Column('realty_user_id', sa.BIGINT, nullable=False),
    sa.Column('master_agent_user_id', sa.BIGINT, nullable=True),
    sa.Column('row_version', sa.BIGINT, nullable=False),
    sa.Column('created_at', sa.TIMESTAMP, nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP, nullable=False),
    sa.Column('first_name', sa.VARCHAR, nullable=True),
    sa.Column('middle_name', sa.VARCHAR, nullable=True),
    sa.Column('last_name', sa.VARCHAR, nullable=True),
)

offers_premoderations = sa.Table(
    'offers_premoderations',
    metadata,
    sa.Column('offer_id', sa.BIGINT, primary_key=True),
    sa.Column('removed', sa.BOOLEAN, nullable=False),
    sa.Column('row_version', sa.BIGINT, nullable=False),
    sa.Column('created_at', sa.TIMESTAMP, nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP, nullable=True),
)

offers_reindex_queue = sa.Table(
    'offers_reindex_queue',
    metadata,
    sa.Column('offer_id', sa.BIGINT, primary_key=True),
    sa.Column('in_process', sa.BOOLEAN, nullable=False),
    sa.Column('created_at', sa.TIMESTAMP, nullable=False),
)
