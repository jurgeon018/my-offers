from datetime import datetime
from typing import List

import asyncpgsa
import pytz
from sqlalchemy.dialects.postgresql import insert

from my_offers import pg
from my_offers.repositories.offers_duplicates.entities import Duplicate
from my_offers.repositories.postgresql import tables


async def update_offers_duplicates(duplicates: List[Duplicate]) -> None:
    now = datetime.now(tz=pytz.UTC)

    data = [
        {
            'offer_id': duplicate.offer_id,
            'group_id': duplicate.duplicate_group_id,
            'created_at': now,
        } for duplicate in duplicates
    ]

    insert_query = insert(tables.offers_duplicates)

    query, params = asyncpgsa.compile_query(
        insert_query
        .values(data)
        .on_conflict_do_nothing()
        # todo: добавить логику https://jira.cian.tech/browse/CD-80218
    )

    await pg.get().execute(query, *params)
