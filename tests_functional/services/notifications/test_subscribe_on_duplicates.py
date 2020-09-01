async def test_public_v1_subscribe_on_duplicates(http, pg):
    # arrange
    user_id = 6808488
    email = 'kek@example.com'

    # act
    await http.request(
        'POST',
        '/public/v1/subscribe-on-duplicates/',
        json={'email': email},
        headers={'X-Real-UserId': user_id},
    )

    # assert
    row = await pg.fetchrow(
        'SELECT * FROM offers_email_notification_settings WHERE user_id = $1', [user_id]
    )

    assert row['user_id'] == user_id
    assert row['email'] == email


async def test_public_v1_subscribe_on_duplicates__invalid_email(http, pg):
    # arrange
    user_id = 6808488
    email = '@example.com'
    expected_message = 'Некорректный email.'

    # act
    response = await http.request(
        'POST',
        '/public/v1/subscribe-on-duplicates/',
        json={'email': email},
        headers={'X-Real-UserId': user_id},
        expected_status=400
    )

    # assert
    assert response.data == {
        'errors': [{
            'key': 'email',
            'code': 'incorrectEmail',
            'message': expected_message
        }],
        'message': expected_message
    }


async def test_public_v1_unsubscribe_on_duplicates__invalid_email(http, pg):
    # arrange
    user_id = 6808488
    email = '@example.com'
    expected_message = 'Некорректный email.'

    # act
    response = await http.request(
        'POST',
        '/public/v1/unsubscribe-on-duplicates/',
        json={'email': email},
        headers={'X-Real-UserId': user_id},
        expected_status=400
    )

    # assert
    assert response.data == {
        'errors': [{
            'key': 'email',
            'code': 'incorrectEmail',
            'message': expected_message
        }],
        'message': expected_message
    }


async def test_public_v1_subscribe_on_duplicates__user_already_subscribed(http, pg):
    # arrange
    user_id = 6808488
    email = 'kek@example.com'
    expected_message = 'Для данного email уже есть активная подписка на уведомления о новых дублях к объектам.'

    await pg.execute(
        'INSERT INTO offers_email_notification_settings (user_id, email) VALUES($1, $2)',
        [user_id, email]
    )

    # act
    response = await http.request(
        'POST',
        '/public/v1/subscribe-on-duplicates/',
        json={'email': email, },
        headers={'X-Real-UserId': user_id},
        expected_status=400
    )

    # assert
    assert response.data == {
        'errors': [{
            'key': 'email',
            'code': 'userAlreadySubscribed',
            'message': expected_message
        }],
        'message': expected_message
    }


async def test_public_v1_unsubscribe_on_duplicates(http, pg):
    # arrange
    user_id = 6808488
    email = 'kek@example.com'

    await pg.execute(
        'INSERT INTO offers_email_notification_settings (user_id, email) VALUES($1, $2)',
        [user_id, email]
    )

    # act
    await http.request(
        'POST',
        '/public/v1/unsubscribe-on-duplicates/',
        json={'email': email, },
        headers={'X-Real-UserId': user_id},
        expected_status=200
    )

    # assert
    row = await pg.fetchrow(
        'SELECT * FROM offers_email_notification_settings WHERE user_id = $1', [user_id]
    )
    assert not row


async def test_public_v1_unsubscribe_on_duplicates__user_not_subscribed(http, pg):
    # arrange
    user_id = 6808488
    email = 'kek@example.com'
    expected_message = 'Для данного email нет активной подписки на уведомления о новых дублях к объектам.'

    # act
    response = await http.request(
        'POST',
        '/public/v1/unsubscribe-on-duplicates/',
        json={'email': email, },
        headers={'X-Real-UserId': user_id},
        expected_status=400
    )

    # assert
    assert response.data == {
        'errors': [{
            'key': 'email',
            'code': 'userIsNotSubscribed',
            'message': expected_message
        }],
        'message': expected_message
    }
