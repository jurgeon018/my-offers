from datetime import datetime

from cian_functional_test_utils.pytest_plugin import MockResponse


async def test_delete_offer__not_found__delete(http, pg, monolith_cian_realty_mock):
    # arrange
    now = datetime.now()
    await pg.execute(
        """
        INSERT INTO offers (
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
            22, 11, 11, 'sale', 'flat', 'notActive', [], True, False, False, 'text',
            '{"id": 11, "category": "flatSale", "status": "Draft"}',
            1, now, now
        ]
    )

    await monolith_cian_realty_mock.add_stub(
        method='POST',
        path='/api/announcement/set-deleted/',
        response=MockResponse(body={'errors': [{'code': 'announcement_not_found'}]}, status=400)
    )

    # act
    response = await http.request(
        'POST',
        'public/v1/actions/delete-offer/',
        headers={
            'X-Real-UserId': 11
        },
        json={
            'offerId': 22
        },
    )

    status_tab = await pg.fetchval('select status_tab from offers where offer_id = 22')

    # assert
    assert response.data == {'status': 'ok'}
    assert status_tab == 'deleted'


async def test_delete_offer__error__error(http, pg, monolith_cian_realty_mock):
    # arrange
    now = datetime.now()
    await pg.execute(
        """
        INSERT INTO offers (
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
            22, 11, 11, 'sale', 'flat', 'notActive', [], True, False, False, 'text',
            '{"id": 11, "category": "flatSale", "status": "Draft"}',
            1, now, now
        ]
    )

    await monolith_cian_realty_mock.add_stub(
        method='POST',
        path='/api/announcement/set-deleted/',
        response=MockResponse(body={'errors': [{'code': 'zzz'}]}, status=400)
    )

    # act
    response = await http.request(
        'POST',
        'public/v1/actions/delete-offer/',
        headers={
            'X-Real-UserId': 11
        },
        json={
            'offerId': 22
        },
        expected_status=400,
    )

    status_tab = await pg.fetchval('select status_tab from offers where offer_id = 22')

    # assert
    assert response.data['errors'][0]['code'] == 'operationError'
    assert status_tab == 'notActive'

