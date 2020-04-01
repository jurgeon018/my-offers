from datetime import datetime
from typing import Dict, List, Optional

import asyncpgsa
from sqlalchemy import and_, update
from sqlalchemy.dialects.postgresql import insert

from my_offers import pg
from my_offers.entities import OfferBillingContract
from my_offers.mappers.billing import offer_billing_contract_mapper
from my_offers.repositories.postgresql.tables import offers_billing_contracts


async def save_offer_contract(offer_contract: OfferBillingContract) -> None:
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
        )
    )

    await pg.get().execute(query, *params)


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


async def get_offer_contract(offer_id: int) -> Optional[OfferBillingContract]:
    query = """
    select
        *
    from
        offers_billing_contracts
    where
        not is_deleted
        and offer_id = $1
    order by
        row_version desc
    limit 1
    """

    result = await pg.get().fetchrow(query, offer_id)

    return offer_billing_contract_mapper.map_from(dict(result)) if result else None


async def get_offers_payed_till(offer_ids: List[int]) -> Dict[int, datetime]:
    query = """
    select
        offer_id,
        max(payed_till) as payed_till
    from
        offers_billing_contracts
    where
        not is_deleted
        and offer_id = any($1::bigint[])
    group by
        offer_id
    """

    rows = await pg.get().fetch(query, offer_ids)

    return {row['offer_id']: row['payed_till'] for row in rows}
