from datetime import datetime, timedelta

import pytz


async def test_v1_has_unread_warnings__200__true__with_last_visit_date(http, pg):
    # arrange
    user_id = 29437831
    now = datetime.now(pytz.utc)

    await pg.execute(
        """
        INSERT INTO public.offers (
            offer_id,
            master_user_id,
            user_id,
            deal_type,
            offer_type,
            status_tab,
            services,
            is_manual,
            is_in_hidden_base,
            has_photo,
            search_text,
            raw_data,
            row_version,
            created_at,
            updated_at
        )
        VALUES
            ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15)
        """,
        [
            123, user_id, user_id, 'sale', 'flat', 'declined', [], True, False, False, 'text',
            '{}', 1, now, now,
        ]
    )

    await pg.execute(
        """
        INSERT INTO public.moderation_alerts (
        user_id, last_visit_date
        )
        VALUES
            ($1, $2)
        """,
        [
            user_id, now - timedelta(hours=1),
        ]
    )

    # act
    response = await http.request(
        'POST',
        '/v1/has-unread-warnings/',
        json={'user_id': user_id},
    )

    # assert
    assert response.data == {'hasWarnings': True}


async def test_v1_has_unread_warnings__200__true__without_last_visit_date(http, pg):
    # arrange
    user_id = 29437831
    now = datetime.now(pytz.utc)

    await pg.execute(
        """
        INSERT INTO public.offers (
            offer_id,
            master_user_id,
            user_id,
            deal_type,
            offer_type,
            status_tab,
            services,
            is_manual,
            is_in_hidden_base,
            has_photo,
            search_text,
            raw_data,
            row_version,
            created_at,
            updated_at
        )
        VALUES
            ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15)
        """,
        [
            123, user_id, user_id, 'sale', 'flat', 'declined', [], True, False, False, 'text',
            '{}', 1, now + timedelta(hours=1), now + timedelta(hours=1),
        ]
    )

    # act
    response = await http.request(
        'POST',
        '/v1/has-unread-warnings/',
        json={'user_id': user_id},
    )

    # assert
    assert response.data == {'hasWarnings': True}


async def test_v1_has_unread_warnings__200__false__with_last_visit_date(http, pg):
    # arrange
    user_id = 29437831
    now = datetime.now(pytz.utc)

    await pg.execute(
        """
        INSERT INTO public.offers (
            offer_id,
            master_user_id,
            user_id,
            deal_type,
            offer_type,
            status_tab,
            services,
            is_manual,
            is_in_hidden_base,
            has_photo,
            search_text,
            raw_data,
            row_version,
            created_at,
            updated_at
        )
        VALUES
            ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15)
        """,
        [
            123, user_id, user_id, 'sale', 'flat', 'declined', [], True, False, False, 'text',
            '{}', 1, now - timedelta(hours=1), now - timedelta(hours=1),
        ]
    )

    await pg.execute(
        """
        INSERT INTO public.moderation_alerts (
        user_id, last_visit_date
        )
        VALUES
            ($1, $2)
        """,
        [
            user_id, now,
        ]
    )

    # act
    response = await http.request(
        'POST',
        '/v1/has-unread-warnings/',
        json={'user_id': user_id},
    )

    # assert
    assert response.data == {'hasWarnings': False}
