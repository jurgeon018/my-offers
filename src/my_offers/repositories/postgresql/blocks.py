from my_offers import pg


async def advisory_lock_for_offer_id(offer_id: int):
    """ https://postgrespro.ru/docs/postgresql/12/functions-admin#FUNCTIONS-ADVISORY-LOCKS
    рекомендательная блокировка pg_advisory_xact_lock действует на уровне транзакции
    и сама снимается после ее завершения"""

    query = """SELECT pg_advisory_xact_lock($1)"""
    await pg.get().execute(query, offer_id)
