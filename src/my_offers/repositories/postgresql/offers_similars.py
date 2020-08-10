import asyncpgsa
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import insert

from my_offers import entities, pg
from my_offers.mappers.offer_mapper import offer_similar_mapper
from my_offers.repositories.postgresql.tables import metadata, offer_type


offers_similars_flat = sa.Table(
    'offers_similars_flat',
    metadata,
    sa.Column('offer_id', sa.BIGINT, primary_key=True),
    sa.Column('offer_type', offer_type, nullable=False),
    sa.Column('group_id', sa.BIGINT, nullable=True),
    sa.Column('house_id', sa.INT, nullable=True),
    sa.Column('district_id', sa.INT, nullable=True),
    sa.Column('price', sa.FLOAT, nullable=True),
    sa.Column('rooms_count', sa.INT, nullable=True),
)


offers_similars_test = sa.Table(
    'offers_similars_test',
    metadata,
    sa.Column('offer_id', sa.BIGINT, primary_key=True),
    sa.Column('offer_type', offer_type, nullable=False),
    sa.Column('group_id', sa.BIGINT, nullable=True),
    sa.Column('house_id', sa.INT, nullable=True),
    sa.Column('district_id', sa.INT, nullable=True),
    sa.Column('price', sa.FLOAT, nullable=True),
    sa.Column('rooms_count', sa.INT, nullable=True),
)


TABLES_MAP = {
    'flat': offers_similars_flat,
    'test': offers_similars_test,
}


async def save(*, suffix: str, similar: entities.OfferSimilar) -> None:
    table = TABLES_MAP[suffix]
    insert_query = insert(table)
    values = offer_similar_mapper.map_to(similar)

    query, params = asyncpgsa.compile_query(
        insert_query
        .values([values])
        .on_conflict_do_update(
            index_elements=[table.c.offer_id],
            set_={
                'offer_type': insert_query.excluded.offer_type,
                'group_id': insert_query.excluded.group_id,
                'house_id': insert_query.excluded.house_id,
                'district_id': insert_query.excluded.district_id,
                'price': insert_query.excluded.price,
                'rooms_count': insert_query.excluded.rooms_count,
            }
        )
    )

    await pg.get().execute(query, *params)


async def delete(*, suffix: str, offer_id: int) -> None:
    table = TABLES_MAP[suffix]
    query, params = asyncpgsa.compile_query(
        sa.delete(table).where(table.c.offer_id == offer_id)
    )

    await pg.get().execute(query, *params)
