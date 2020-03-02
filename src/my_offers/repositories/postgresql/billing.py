from typing import Optional

import asyncpgsa
from sqlalchemy import and_, select, update
from sqlalchemy.dialects.postgresql import insert

from my_offers import pg
from my_offers.entities import AnnouncementBillingContract
from my_offers.entities.billing import OfferBillingContract
from my_offers.mappers.billing import offer_billing_contract_mapper
from my_offers.repositories.postgresql.tables import offers_billing_contracts


async def save_offer_contract(offer_contract: AnnouncementBillingContract) -> None:
    values = {
        'id': offer_contract.id,
        'user_id': offer_contract.user_id,
        'actor_user_id': offer_contract.actor_user_id,
        'publisher_user_id': offer_contract.publisher_user_id,
        'target_object_id': offer_contract.target_object_id,
        'target_object_type': offer_contract.target_object_type.name,
        'start_date': offer_contract.start_date,
        'payed_till': offer_contract.payed_till,
        'row_version': offer_contract.row_version,
        'is_deleted': False,
    }

    query, params = asyncpgsa.compile_query(
        insert(
            offers_billing_contracts
        ).values([
            values
        ]).on_conflict_do_update(
            index_elements=[offers_billing_contracts.c.id],
            where=offers_billing_contracts.c.row_version < offer_contract.row_version,
            set_=values
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


async def get_offer_contract(contract_id: int) -> Optional[OfferBillingContract]:
    sql = (
        select([
            offers_billing_contracts
        ]).where(
            offers_billing_contracts.c.id == contract_id
        )
    )
    query, params = asyncpgsa.compile_query(sql)
    result = await pg.get().fetchrow(query, *params)

    return offer_billing_contract_mapper.map_from(dict(result)) if result else None
