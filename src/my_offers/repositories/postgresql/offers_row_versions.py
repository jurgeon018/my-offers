from typing import Any, Dict, List

import asyncpgsa
from sqlalchemy.dialects.postgresql import insert

from my_offers import pg
from my_offers.mappers.changed_announcement import changed_announcement_map_from
from my_offers.repositories.monolith_cian_ms_announcements.entities import ChangedAnnouncement
from my_offers.repositories.postgresql.tables import offers_row_versions


async def clean_offer_row_versions() -> None:
    await pg.get().execute('delete from offers_row_versions')


async def save_offer_row_versions(offer_versions: List[ChangedAnnouncement]) -> None:
    data: Dict[int, Any] = {}
    for offer_version in offer_versions:
        if (
            offer_version.id not in data
            or data[offer_version.id]['row_version'] < offer_version.row_version
        ):
            data[offer_version.id] = changed_announcement_map_from(offer_version)

    insert_query = insert(offers_row_versions)
    query, params = asyncpgsa.compile_query(
        insert_query
        .values(list(data.values()))
        .on_conflict_do_update(
            index_elements=[offers_row_versions.c.offer_id],
            set_={
                'row_version': insert_query.excluded.row_version,
                'status_tab': insert_query.excluded.status_tab,
            }
        )
    )

    await pg.get().execute(query, *params)


async def get_outdated_offer_ids() -> List[int]:
    """
    Выбираем все объявления у которы в С# версия выше
    пропускаем архивные и удаленные
    """
    query = """
    select
        o.offer_id
    from
        offers o
        left join offers_row_versions orv on o.offer_id = orv.offer_id
    where
        o.row_version < orv.row_version
        and not (o.status_tab = 'archived' and orv.status_tab = 'archived')
        and not (o.status_tab = 'deleted' and orv.status_tab = 'deleted')
        and not o.is_test
    order by
        o.offer_id
    """

    result = await pg.get().fetch(query)

    return [item['offer_id'] for item in result]


async def get_offer_ids(limit: int, last_offer_id: int = 0) -> List[int]:
    """
    Выбираем все объявления
    пропускаем архивные и удаленные
    """
    query = """
    select
        o.offer_id
    from
        offers o
        left join offers_row_versions orv on o.offer_id = orv.offer_id
    where
        o.offer_id > $1
        and not (o.status_tab = 'archived' and orv.status_tab = 'archived')
        and not (o.status_tab = 'deleted' and orv.status_tab = 'deleted')
        and not o.is_test
    order by
        o.offer_id
    limit $2
    """
    params = (last_offer_id, limit)

    rows = await pg.get().fetch(query, *params)

    return [row['offer_id'] for row in rows]


async def get_missed_offer_ids() -> List[int]:
    """
    Выбираем все которые есть в С#, но отсутствуют у нас
    """
    query = """
    select
        orv.offer_id
    from
        offers_row_versions orv
        left join offers o on o.offer_id = orv.offer_id
    where
        o.row_version is null
        and orv.status_tab not in ('archived', 'deleted')
    """

    result = await pg.get().fetch(query)

    return [item['offer_id'] for item in result]


async def get_offers_ids_to_archive() -> List[int]:
    query = """
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
    """

    result = await pg.get().fetch(query)

    return [item['offer_id'] for item in result]
