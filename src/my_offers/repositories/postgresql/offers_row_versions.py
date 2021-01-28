from typing import List

import asyncpgsa
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import insert

from my_offers import pg
from my_offers.repositories.monolith_cian_ms_announcements.entities import ChangedAnnouncement
from my_offers.repositories.postgresql.tables import metadata


offers_row_versions = sa.Table(
    'offers_row_versions',
    metadata,
    sa.Column('offer_id', sa.BIGINT, primary_key=True),
    sa.Column('row_version', sa.BIGINT, nullable=False),
)


async def clean_offer_row_versions() -> None:
    await pg.get().execute('delete from offers_row_versions')


async def save_offer_row_versions(offer_versions: List[ChangedAnnouncement]) -> None:
    data = []
    for offer_version in offer_versions:
        data.append({
            'offer_id': offer_version.id,
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


async def get_outdated_offer_ids() -> List[int]:
    query = """
    select
        o.offer_id
    from
        offers o
        left join offers_row_versions orv on o.offer_id = orv.offer_id
    where
        o.row_version < orv.row_version
        and not o.is_test
    order by
        o.offer_id
    """

    result = await pg.get().fetch(query)

    return [item['offer_id'] for item in result]


async def archive_missed_offers() -> None:
    query = """
    update
        offers
    set
        status_tab = 'archived'
    where
        offer_id in (
            select
                o.offer_id
            from
                offers o
                left join offers_row_versions orv on o.offer_id = orv.offer_id
            where
                orv.row_version is null
                and o.row_version < (select max(row_version) from offers_row_versions)
                and o.status_tab not in ('deleted', 'archived')
                and not o.is_test
        )
    """

    await pg.get().execute(query)
