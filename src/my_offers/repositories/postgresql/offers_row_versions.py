from typing import List

import asyncpgsa
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import insert

from my_offers import pg
from my_offers.repositories.monolith_cian_elasticapi.entities import ElasticAnnouncementRowVersion
from my_offers.repositories.postgresql.tables import metadata


offers_row_versions = sa.Table(
    'offers_row_versions',
    metadata,
    sa.Column('offer_id', sa.BIGINT, primary_key=True),
    sa.Column('row_version', sa.BIGINT, nullable=False),
)


async def save_offer_row_versions(offer_versions: List[ElasticAnnouncementRowVersion]) -> None:
    data = []
    for offer_version in offer_versions:
        data.append({
            'offer_id': offer_version.realty_object_id,
            'row_version': offer_version.row_version,
        })

    insert_query = insert(offers_row_versions)
    query, params = asyncpgsa.compile_query(
        insert_query
        .values(data)
        .on_conflict_do_update(
            index_elements=[offers_row_versions.c.offer_id],
            set_={'row_version': insert_query.excluded.row_version}
        )
    )

    await pg.get().execute(query, *params)
