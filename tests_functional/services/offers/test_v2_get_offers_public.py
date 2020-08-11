import json
from datetime import datetime
from pathlib import Path

import pytest


async def test_v2_get_offers_public__not_found__200(http_client):
    # act
    response = await http_client.request(
        'POST',
        '/public/v2/get-offers/',
        json={
            'filters': {
                'statusTab': 'active',
                'searchText': '+7 (929) 444 55-77 Москва'
            }
        },
        headers={
            'X-Real-UserId': 13933440
        },
    )

    # assert
    assert len(response.data['offers']) == 0


async def test_v2_get_offers_public__search_text__result(http_client, pg):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')

    # act
    response = await http_client.request(
        'POST',
        '/public/v2/get-offers/',
        json={
            'filters': {
                'statusTab': 'active',
                'searchText': '+7 (962) 078 83-57 Красноярский край'
            }
        },
        headers={
            'X-Real-UserId': 29437831
        },
    )

    # assert
    assert response.data['offers'][0]['id'] == 209194477


@pytest.mark.parametrize('x_real_user, can_change_publisher', [
    (333, True),
    (222, False),
])
async def test_v2_get_offers_public__can_change_publisher(http_client, pg, x_real_user, can_change_publisher):
    # arrange
    offer_id_1 = 11111111
    user_id = 222
    master_user = 333

    now = datetime.now()
    await pg.execute(
        """
        INSERT INTO public.agents_hierarchy (
            id,
            row_version,
            realty_user_id,
            master_agent_user_id,
            created_at,
            updated_at,
            account_type
        )
        VALUES
            ($1, $2, $3, $4, $5, $6, $7),
            ($8, $9, $10, $11, $12, $13, $14)
        """,
        [
            1, 123, user_id, master_user, now, now, 'Specialist',
            2, 123, master_user, None, now, now, 'Agency'
        ]
    )

    offer_json = json.dumps({
        "id": offer_id_1,
        "status": "Published",
        "category": "flatRent",
        "bargainTerms": {
            "currency": "rur"
        }
    })

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
            offer_id_1, master_user, user_id, 'sale', 'flat', 'active', [], True, False, False, 'text',
            offer_json, 1, now, now,
        ]
    )

    # act
    response = await http_client.request(
        'POST',
        '/public/v2/get-offers/',
        json={
            'filters': {
                'statusTab': 'active',
            }
        },
        headers={
            'X-Real-UserId': x_real_user
        },
    )

    # assert
    assert response.data['offers'][0]['id'] == 11111111
    assert response.data['offers'][0]['availableActions']['canChangePublisher'] is can_change_publisher
