from typing import List

from my_offers import pg
import sqlalchemy as sa


async def delete_rows_by_offer_id(table_name: sa.Table.name, offer_ids: List[int]) -> None:
    query = 'DELETE FROM $1 WHERE offer_id = ANY($2::BIGINT[])'
    await pg.get().execute(query, table_name, offer_ids)
