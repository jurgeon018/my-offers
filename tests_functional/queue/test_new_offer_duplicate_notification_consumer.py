import asyncio
import json
import uuid
from pathlib import Path

from cian_functional_test_utils.pytest_plugin import MockResponse


async def test_new_offer_duplicate_notification_consumer(queue_service, pg, kafka_service, notification_center_mock):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')
    await pg.execute('INSERT INTO offers_duplicates values(231655140, 231655140, \'2020-05-09\')')
    await pg.execute('INSERT INTO offers_duplicates values(173975523, 231655140, \'2020-05-09\')')

    await notification_center_mock.add_stub(
        method='POST',
        path='/v1/mobile-push/get-settings/',
        response=MockResponse(
            body={
                'items': [
                    {
                        'children': [
                            {'description': '',
                             'id': 'OfferNewDuplicateFoundNotifications',
                             'isActive': True,
                             'title': 'Новые дубли по объектам'}
                        ],
                        'id': 'OfferDuplicatesGroup',
                        'title': 'Дубли по вашим объектам'
                    }
                ]
            }
        ),
    )
    notification_center_stub = await notification_center_mock.add_stub(
        method='POST',
        path='/v2/register-notifications/',
        response=MockResponse(),
    )

    message = {
        'duplicateOfferId': 231655140,
        'date': '2020-05-27T15:07:35.005788+00:00',
        'operationId': 'c31e2bb8-a02b-11ea-a141-19840ed2f005'
    }

    await queue_service.wait_consumer('my-offers.new_offer_duplicate_notification')

    # act
    await queue_service.publish('my-offers.offer-duplicate.v1.new', message, exchange='my-offers')
    await asyncio.sleep(1)
    messages = await kafka_service.get_messages(topic='myoffer-specialist-push-notification')

    # assert
    request = await notification_center_stub.get_request()
    assert request.data == {
        'notifications': [
            {
                'emailPayload': None,
                'entityId': 173975523,
                'isAuthenticated': True,
                'mediaUrl': 'https://cdn-p.cian.site/images/1/644/244/kvartira-tula-prospekt-lenina-442446187-3.jpg',
                'mobilePushPayload': {
                    'dealType': 'rent',
                    'offerType': 'flat',
                    'duplicateOfferId': 231655140,
                },
                'notificationType': 'offerNewDuplicateFound',
                'plannedSendDatetime': None,
                'text': 'Тульская область, Тула, проспект Ленина, 130',
                'title': 'Новый дубль вашего объекта',
                'transportsToSend': ['mobilePush'],
                'userId': '6808488',
                'webPushPayload': None,
                'webUrl': 'http://master.dev3.cian.ru/rent/flat/231655140'
            }
        ]
    }

    assert len(messages) == 1
    payload = json.loads(messages[0].payload)
    payload.pop('timestamp', None)
    assert payload == {
        'similarObjectPrice': 1350000,
        'similarObjectId': 231655140,
        'userId': 6808488,
        'eventType': 'pushOfferDuplicate',
        'objectId': 173975523,
        'operationId': 'c31e2bb8-a02b-11ea-a141-19840ed2f005',
        'regionId': 4592,
        'transport': 'mobilePush',
    }


async def test_new_offer_duplicate_notification_consumer__push_disabled__skip(
        queue_service, pg, notification_center_mock
):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')
    await pg.execute('INSERT INTO offers_duplicates values(231655140, 231655140, \'2020-05-09\')')
    await pg.execute('INSERT INTO offers_duplicates values(173975523, 231655140, \'2020-05-09\')')

    await notification_center_mock.add_stub(
        method='POST',
        path='/v1/mobile-push/get-settings/',
        response=MockResponse(
            body={
                'items': []
            }
        ),
    )

    message = {
        'duplicateOfferId': 231655140,
        'date': '2020-05-27T15:07:35.005788+00:00',
        'operationId': 'c31e2bb8-a02b-11ea-a141-19840ed2f005'
    }

    await queue_service.wait_consumer('my-offers.new_offer_duplicate_notification')

    # act & assert
    await queue_service.publish('my-offers.offer-duplicate.v1.new', message, exchange='my-offers')


async def test_new_offer_duplicate_notification_consumer__already_sent(queue_service, pg, notification_center_mock):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')
    await pg.execute('INSERT INTO offers_duplicates values(231655140, 231655140, \'2020-05-09\')')
    await pg.execute('INSERT INTO offers_duplicates values(173975523, 231655140, \'2020-05-09\')')

    await pg.execute('INSERT INTO offers_duplicate_notification values(173975523, 231655140, \'2020-05-09\')')

    notification_center_stub = await notification_center_mock.add_stub(
        method='POST',
        path='/v2/register-notifications/',
        response=MockResponse(),
    )

    message = {
        'duplicateOfferId': 231655140,
        'date': '2020-05-27T15:07:35.005788+00:00',
        'operationId': 'c31e2bb8-a02b-11ea-a141-19840ed2f005'
    }

    await queue_service.wait_consumer('my-offers.new_offer_duplicate_notification')

    # act
    await queue_service.publish('my-offers.offer-duplicate.v1.new', message, exchange='my-offers')
    await asyncio.sleep(1)

    # assert
    assert not await notification_center_stub.get_requests()


async def test_new_offer_duplicate_notification_consumer__error(queue_service, pg, notification_center_mock):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')
    await pg.execute('INSERT INTO offers_duplicates values(231655140, 231655140, \'2020-05-09\')')
    await pg.execute('INSERT INTO offers_duplicates values(173975523, 231655140, \'2020-05-09\')')

    await notification_center_mock.add_stub(
        method='POST',
        path='/v1/mobile-push/get-settings/',
        response=MockResponse(
            body={
                'items': [
                    {
                        'children': [
                            {'description': '',
                             'id': 'OfferNewDuplicateFoundNotifications',
                             'isActive': True,
                             'title': 'Новые дубли по объектам'}
                        ],
                        'id': 'OfferDuplicatesGroup',
                        'title': 'Дубли по вашим объектам'
                    }
                ]
            }
        ),
    )
    notification_center_stub = await notification_center_mock.add_stub(
        method='POST',
        path='/v2/register-notifications/',
        response=MockResponse(status=500),
    )

    message = {
        'duplicateOfferId': 231655140,
        'date': '2020-05-27T15:07:35.005788+00:00',
        'operationId': 'c31e2bb8-a02b-11ea-a141-19840ed2f005'
    }

    await queue_service.wait_consumer('my-offers.new_offer_duplicate_notification')

    # act
    await queue_service.publish('my-offers.offer-duplicate.v1.new', message, exchange='my-offers')
    await asyncio.sleep(1)

    # assert
    request = await notification_center_stub.get_request()
    assert len(request.data['notifications']) == 1

    row = await pg.fetchrow('SELECT * FROM offers_duplicate_notification WHERE offer_id = 173975523')
    assert row is None


async def test_new_offer_duplicate_notification_consumer__offer_not_found(queue_service, pg, notification_center_mock):
    # arrange
    await pg.execute('INSERT INTO offers_duplicates values(231655140, 231655140, \'2020-05-09\')')
    await pg.execute('INSERT INTO offers_duplicates values(173975523, 231655140, \'2020-05-09\')')

    notification_center_stub = await notification_center_mock.add_stub(
        method='POST',
        path='/v2/register-notifications/',
        response=MockResponse(),
    )

    message = {
        'duplicateOfferId': 231655140,
        'date': '2020-05-27T15:07:35.005788+00:00',
        'operationId': 'c31e2bb8-a02b-11ea-a141-19840ed2f005'
    }

    await queue_service.wait_consumer('my-offers.new_offer_duplicate_notification')

    # act
    await queue_service.publish('my-offers.offer-duplicate.v1.new', message, exchange='my-offers')
    await asyncio.sleep(1)

    # assert
    assert not await notification_center_stub.get_requests()


async def test_new_offer_duplicate_notification_consumer__email_push(
        queue_service,
        pg,
        kafka_service,
        notification_center_mock,
        emails_mock
):
    # arrange
    user_id = 6808488
    email = 'kek@example.com'

    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')
    await pg.execute('INSERT INTO offers_duplicates values(231655140, 231655140, \'2020-05-09\')')
    await pg.execute('INSERT INTO offers_duplicates values(173975523, 231655140, \'2020-05-09\')')
    await pg.execute(
        'INSERT INTO offers_email_notification_settings (user_id, email) VALUES($1, $2)',
        [user_id, email]
    )
    await notification_center_mock.add_stub(
        method='POST',
        path='/v1/mobile-push/get-settings/',
        response=MockResponse(
            body={'items': []}
        ),
    )
    await emails_mock.add_stub(
        method='POST',
        path='/emails/v2/send-email/',
        response=MockResponse(
            body={
                'items': [],
                'status': 'success'
            }
        ),
    )

    message = {
        'duplicateOfferId': 231655140,
        'date': '2020-05-27T15:07:35.005788+00:00',
        'operationId': 'c31e2bb8-a02b-11ea-a141-19840ed2f005'
    }

    await queue_service.wait_consumer('my-offers.new_offer_duplicate_notification')

    # act
    await queue_service.publish('my-offers.offer-duplicate.v1.new', message, exchange='my-offers')
    await asyncio.sleep(1)
    messages = await kafka_service.get_messages(topic='myoffer-specialist-push-notification')

    # assert
    assert len(messages) == 1
    payload = json.loads(messages[0].payload)
    payload.pop('timestamp', None)
    assert payload == {
        'similarObjectPrice': 1350000,
        'similarObjectId': 231655140,
        'userId': 6808488,
        'eventType': 'pushOfferDuplicate',
        'objectId': 173975523,
        'operationId': 'c31e2bb8-a02b-11ea-a141-19840ed2f005',
        'regionId': 4592,
        'transport': 'emailPush',
    }


async def test_new_offer_duplicate_notification_consumer__send_all_notifications(
        queue_service,
        pg,
        kafka_service,
        notification_center_mock,
        emails_mock
):
    """ Проверяем отсылку нескольких типов уведомлений для одного пользователя """
    # arrange
    user_id = 6808488
    email = 'kek@example.com'

    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')
    await pg.execute('INSERT INTO offers_duplicates values(231655140, 231655140, \'2020-05-09\')')
    await pg.execute('INSERT INTO offers_duplicates values(173975523, 231655140, \'2020-05-09\')')
    await pg.execute(
        'INSERT INTO offers_email_notification_settings (user_id, email) VALUES($1, $2)',
        [user_id, email]
    )
    await notification_center_mock.add_stub(
        method='POST',
        path='/v1/mobile-push/get-settings/',
        response=MockResponse(
            body={
                'items': [
                    {
                        'children': [
                            {'description': '',
                             'id': 'OfferNewDuplicateFoundNotifications',
                             'isActive': True,
                             'title': 'Новые дубли по объектам'}
                        ],
                        'id': 'OfferDuplicatesGroup',
                        'title': 'Дубли по вашим объектам'
                    }
                ]
            }
        ),
    )
    await notification_center_mock.add_stub(
        method='POST',
        path='/v2/register-notifications/',
        response=MockResponse(),
    )
    await emails_mock.add_stub(
        method='POST',
        path='/emails/v2/send-email/',
        response=MockResponse(
            body={
                'items': [],
                'status': 'success'
            }
        ),
    )

    message = {
        'duplicateOfferId': 231655140,
        'date': '2020-05-27T15:07:35.005788+00:00',
        'operationId': 'c31e2bb8-a02b-11ea-a141-19840ed2f005'
    }

    await queue_service.wait_consumer('my-offers.new_offer_duplicate_notification')

    # act
    await queue_service.publish('my-offers.offer-duplicate.v1.new', message, exchange='my-offers')
    await asyncio.sleep(2)

    # assert
    rows = await pg.fetch('SELECT * FROM offers_duplicate_notification')
    assert rows[0]['offer_id'] == 173975523
    assert rows[0]['duplicate_offer_id'] == 231655140
    assert rows[0]['notification_type'] == 'mobilePush'
    assert rows[1]['offer_id'] == 173975523
    assert rows[1]['duplicate_offer_id'] == 231655140
    assert rows[1]['notification_type'] == 'emailPush'
