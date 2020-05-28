from datetime import datetime

import pytest


@pytest.mark.parametrize('status_tab, with_subs, user_id, expected', (
    ('active', False, 1, 0),
    ('active', False, 2, 1),
    ('all', False, 2, 2),
    ('all', True, 2, 3),
))
async def test_get_offers_count_by_tab(pg, http_client, status_tab, with_subs, user_id, expected):
    # arrange
    now = datetime.now()
    await pg.execute(
        """
        INSERT INTO public.agents_hierarchy (
            id,
            row_version,
            realty_user_id,
            master_agent_user_id,
            created_at,
            updated_at
        )
        VALUES
            ($1, $2, $3, $4, $5, $6)
        """,
        [1, 123, 2, 2, now, now],
    )
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
            ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15),
            ($16, $17, $18, $19, $20, $21, $22, $23, $24, $25, $26, $27, $28, $29, $30),
            ($31, $32, $33, $34, $35, $36, $37, $38, $39, $40, $41, $42, $43, $44, $45)
        """,
        [
            1, 2, 2, 'sale', 'flat', 'active', [], True, False, False, 'text', '{}', 1, now, now,
            2, 2, 3, 'sale', 'flat', 'active', [], True, False, False, 'text', '{}', 1, now, now,
            3, 2, 2, 'sale', 'flat', 'deleted', [], True, False, False, 'text', '{}', 1, now, now,
        ]
    )

    # act
    response = await http_client.request(
        'POST',
        '/v1/get-offers-count-by-tab/',
        json={
            'statusTab': status_tab,
            'userId': user_id,
            'withSubs': with_subs,
        },
    )

    # assert
    assert response.data['count'] == expected
