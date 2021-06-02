from datetime import datetime


async def test_v1_hide_warnings__200(http, pg):
    # arrange
    user_id = 29437831

    # act
    response = await http.request(
        'POST',
        '/public/v1/hide-warnings/',
        headers={
            'X-Real-UserId': user_id
        },
        json={'tabType': 'declined'},
    )

    row = await pg.fetchrow('SELECT * FROM moderation_alerts')

    # assert
    assert response.body == b''
    assert row['user_id'] == user_id
    assert row['last_visit_date'].date() == datetime.now().date()


async def test_v1_hide_warnings__200__update_record(http, pg):
    # arrange
    user_id = 29437832

    # act
    first_response = await http.request(
        'POST',
        '/public/v1/hide-warnings/',
        headers={
            'X-Real-UserId': user_id
        },
        json={'tabType': 'declined'},
    )

    second_response = await http.request(
        'POST',
        '/public/v1/hide-warnings/',
        headers={
            'X-Real-UserId': user_id
        },
        json={'tabType': 'declined'},
    )

    row = await pg.fetchrow('SELECT * FROM moderation_alerts')

    # assert
    assert first_response.body == b''
    assert second_response.body == b''
    assert row['user_id'] == user_id
    assert row['last_visit_date'].date() == datetime.now().date()
