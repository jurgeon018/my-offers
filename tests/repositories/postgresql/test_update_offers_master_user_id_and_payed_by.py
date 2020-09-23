from my_offers import pg
from my_offers.repositories.postgresql import update_offers_master_user_id_and_payed_by


async def test_update_offers_master_user_id_and_payed_by():
    # arrange
    offer_ids = [1, 2, 3]
    query = """
        with cte as (
        select
            a.offer_id, b.master_agent_user_id, c.publisher_user_id
        from
            offers as a
        inner join
            agents_hierarchy as b on a.user_id = b.realty_user_id
        inner join
            offers_billing_contracts as c on a.offer_id = c.offer_id
        where a.offer_id = ANY($1::BIGINT[])
        )

        update
            offers
        set
            old_master_user_id = master_user_id,
            master_user_id = COALESCE(cte.master_agent_user_id, cte.publisher_user_id),
            payed_by = cte.publisher_user_id
        from
            cte
        where
            offers.offer_id = cte.offer_id
    """

    # act
    await update_offers_master_user_id_and_payed_by(offer_ids)

    # arrange
    pg.get().execute.assert_called_once_with(query, offer_ids)
