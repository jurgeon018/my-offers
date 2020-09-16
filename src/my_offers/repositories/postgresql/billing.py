from datetime import datetime
from typing import Dict, List, Optional

import asyncpgsa
from simple_settings import settings
from sqlalchemy import and_, any_, not_, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql import func

from my_offers import enums, pg
from my_offers.entities import OfferBillingContract
from my_offers.enums import OfferServiceTypes
from my_offers.mappers.billing import offer_billing_contract_mapper
from my_offers.repositories.postgresql import tables
from my_offers.repositories.postgresql.tables import offers_billing_contracts


async def save_offer_contract(offer_contract: OfferBillingContract) -> Optional[int]:
    insert_values = offer_billing_contract_mapper.map_to(offer_contract)

    # меняем только дату обновления контракта для update
    update_values = insert_values.copy()
    update_values.pop('created_at', None)

    query, params = asyncpgsa.compile_query(
        insert(
            offers_billing_contracts
        ).values([
            insert_values
        ]).on_conflict_do_update(
            index_elements=[offers_billing_contracts.c.id],
            where=offers_billing_contracts.c.row_version < offer_contract.row_version,
            set_=update_values
        ).returning(
            offers_billing_contracts.c.id
        )
    )

    row = await pg.get().fetchrow(query, *params)

    return row['id'] if row else None


async def set_offer_contract_is_deleted_status(*, contract_id: int, row_version: int) -> None:
    sql = (
        update(
            offers_billing_contracts
        ).values({
            'is_deleted': True
        }).where(and_(
            offers_billing_contracts.c.row_version < row_version,
            offers_billing_contracts.c.id == contract_id
        ))
    )
    query, params = asyncpgsa.compile_query(sql)

    await pg.get().execute(query, *params)


async def get_offers_payed_till(offer_ids: List[int],
                                exclude_service_type: Optional[OfferServiceTypes] = None) -> Dict[int, datetime]:
    """ Вытаскиваем из базы даты окончания оплаты для списка объявлений.
        У одного объявления может быть несколько контрактов, берется максимальная дата
        и при этом исключаются контракты с переданной услугой.
    """

    collumn = tables.offers_billing_contracts.c
    options = [
        not_(collumn.is_deleted),
        collumn.offer_id == any_(offer_ids)
    ]

    if exclude_service_type:
        options.append(exclude_service_type != any_(collumn.service_types))

    query, params = asyncpgsa.compile_query(
        select((
            collumn.offer_id,
            func.max(collumn.payed_till).label('payed_till')
        )).where(
            and_(
                *options
                )
        ).group_by(collumn.offer_id)
    )

    rows = await pg.get().fetch(query, *params, timeout=settings.DB_TIMEOUT)

    return {row['offer_id']: row['payed_till'] for row in rows}


async def get_offers_payed_till_excluding_calltracking(offer_ids: List[int]) -> Dict[int, datetime]:
    """ Вытаскиваем из базы дату окончания оплаты для объявлений, исключая
        контракты с услугой calltracking. Сделано для отображения пользователям
        корректного числа оставшихся дней публикации объявления
    """

    return await get_offers_payed_till(
        offer_ids,
        enums.OfferServiceTypes.calltracking.value
    )


async def get_offer_publisher_user_id(offer_id: int) -> Optional[int]:
    query = """
    select
        publisher_user_id
    from
        offers_billing_contracts
    where
        offer_id = $1
    order by
        row_version desc
    limit
        1
    """

    row = await pg.get().fetchrow(query, offer_id)

    return row['publisher_user_id'] if row else None
