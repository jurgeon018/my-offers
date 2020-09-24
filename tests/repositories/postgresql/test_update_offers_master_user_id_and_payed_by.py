from my_offers import pg
from my_offers.repositories.postgresql import update_offers_master_user_id_and_payed_by


async def test_update_offers_master_user_id_and_payed_by():
    # arrange
    offer_ids = [1, 2, 3]
    query = """
        with cte1 as (
        select
            a.offer_id, b.master_agent_user_id
        from
            offers as a
        inner join
            agents_hierarchy as b on a.user_id = b.realty_user_id
        where
            a.offer_id = ANY($1::BIGINT[])
        ), cte2 as (
        select
            c.offer_id, first_value (publisher_user_id)
                        over (partition by offer_id order by row_version desc) as publisher_user_id
        from
            offers_billing_contracts as c
        where
            c.offer_id = ANY($1::BIGINT[])
        )

        update
            offers
        set
            old_master_user_id = master_user_id,
            master_user_id = COALESCE(cte1.master_agent_user_id, cte2.publisher_user_id),
            payed_by = cte2.publisher_user_id
        from
            cte1
        inner join
            cte2
        on
            cte1.offer_id = cte2.offer_id
        where
            offers.offer_id = cte1.offer_id
    """

    # act
    await update_offers_master_user_id_and_payed_by(offer_ids)

    # arrange
    pg.get().execute.assert_called_once_with(query, offer_ids)
