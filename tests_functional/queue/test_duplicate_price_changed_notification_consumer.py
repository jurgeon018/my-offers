import asyncio
import json
from pathlib import Path

from cian_functional_test_utils.pytest_plugin import MockResponse


async def test_offer_duplicate_price_changed_notification_consumer__price_increased__send_push_ok(
        queue_service,
        pg,
        kafka_service,
        notification_center_mock,
):
    # arrange
    await queue_service.wait_consumer('my-offers.offer_duplicate_price_changed_notification', timeout=300)
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')
    await pg.execute('INSERT INTO offers_duplicates values(231655140, 231655140, \'2020-05-09\')')
    await pg.execute('INSERT INTO offers_duplicates values(173975523, 231655140, \'2020-05-09\')')
    await pg.execute(
        """
        INSERT INTO public.offers_similars_flat (
            offer_id, group_id, house_id, district_id, price,
            rooms_count, deal_type, sort_date, old_price
        )
        VALUES
            (231655140, 231655140, NULL , 341, 1350000.0, 2, 'sale', \'2020-05-09\', 1000000.0)
        """)

    await notification_center_mock.add_stub(
        method='POST',
        path='/v1/mobile-push/get-settings/',
        response=MockResponse(
            body={
                'items': [
                    {
                        'children': [
                            {'description': '',
                             'id': 'DuplicatePriceChangedNotifications',
                             'isActive': True,
                             'title': 'Изменения цены в дублях'}
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

    await queue_service.wait_consumer('my-offers.offer_duplicate_price_changed_notification')

    # act
    await queue_service.publish('my-offers.offer-duplicate.v1.price_changed', message, exchange='my-offers')
    await asyncio.sleep(1)

    # assert
    request_notification = await notification_center_stub.get_request()
    assert request_notification.data == {
        'notifications': [
            {
                'emailPayload': None,
                'entityId': 173975523,
                'isAuthenticated': True,
                'mediaUrl': 'https://cdn-p.cian.site/images/1/644/244/kvartira-tula-prospekt-lenina-442446187-3.jpg',
                'mobilePushPayload': {
                    'dealType': 'rent',
                    'offerType': 'flat',
                    'priceChangeButtonText': 'Изменить мою цену'
                },
                'notificationType': 'duplicatePriceChanged',
                'plannedSendDatetime': None,
                'text': 'Тульская область, Тула, проспект Ленина, 130',
                'title': 'Цена на дубль увеличена до\xa01\xa0350\xa0000\xa0₽',
                'transportsToSend': ['mobilePush'],
                'userId': '6808488',
                'webPushPayload': None,
                'webUrl': 'http://master.dev3.cian.ru/rent/flat/231655140'
            }
        ]
    }


async def test_offer_duplicate_price_changed_notification_consumer__price_reduced__send_push_ok(
        queue_service,
        pg,
        kafka_service,
        notification_center_mock,
):
    # arrange
    await queue_service.wait_consumer('my-offers.offer_duplicate_price_changed_notification', timeout=300)
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')
    await pg.execute('INSERT INTO offers_duplicates values(231655140, 231655140, \'2020-05-09\')')
    await pg.execute('INSERT INTO offers_duplicates values(173975523, 231655140, \'2020-05-09\')')
    await pg.execute(
        """
        INSERT INTO public.offers_similars_flat (
            offer_id, group_id, house_id, district_id, price,
            rooms_count, deal_type, sort_date, old_price
        )
        VALUES
            (231655140, 231655140, NULL , 341, 1350000.0, 2, 'sale', \'2020-05-09\', 2000000.0)
        """)

    await notification_center_mock.add_stub(
        method='POST',
        path='/v1/mobile-push/get-settings/',
        response=MockResponse(
            body={
                'items': [
                    {
                        'children': [
                            {'description': '',
                             'id': 'DuplicatePriceChangedNotifications',
                             'isActive': True,
                             'title': 'Изменения цены в дублях'}
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

    await queue_service.wait_consumer('my-offers.offer_duplicate_price_changed_notification')

    # act
    await queue_service.publish('my-offers.offer-duplicate.v1.price_changed', message, exchange='my-offers')
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
                    'priceChangeButtonText': 'Изменить мою цену'
                },
                'notificationType': 'duplicatePriceChanged',
                'plannedSendDatetime': None,
                'text': 'Тульская область, Тула, проспект Ленина, 130',
                'title': 'Цена на дубль снижена до\xa01\xa0350\xa0000\xa0₽',
                'transportsToSend': ['mobilePush'],
                'userId': '6808488',
                'webPushPayload': None,
                'webUrl': 'http://master.dev3.cian.ru/rent/flat/231655140'
            }
        ]
    }
    payload = json.loads(messages[0].payload)
    payload.pop('timestamp', None)
    assert payload == {
        'similarObjectPrice': 1350000,
        'similarObjectId': 231655140,
        'userId': 6808488,
        'eventType': 'pushPriceChangeOfferDuplicate',
        'objectId': 173975523,
        'operationId': 'c31e2bb8-a02b-11ea-a141-19840ed2f005',
        'regionId': 4592,
        'transport': 'mobilePush',
    }


async def test_duplicate_price_changed_consumer__same_price_and_old_price__push_not_sent(
        queue_service,
        pg,
        kafka_service,
        notification_center_mock,
):
    # arrange
    await queue_service.wait_consumer('my-offers.offer_duplicate_price_changed_notification', timeout=300)
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')
    await pg.execute('INSERT INTO offers_duplicates values(231655140, 231655140, \'2020-05-09\')')
    await pg.execute('INSERT INTO offers_duplicates values(173975523, 231655140, \'2020-05-09\')')
    await pg.execute(
        """
        INSERT INTO public.offers_similars_flat (
            offer_id, group_id, house_id, district_id, price,
            rooms_count, deal_type, sort_date, old_price
        )
        VALUES
            (231655140, 231655140, NULL , 341, 1350000.0, 2, 'sale', \'2020-05-09\', 1350000.0)
        """)

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

    await queue_service.wait_consumer('my-offers.offer_duplicate_price_changed_notification')

    # act
    await queue_service.publish('my-offers.offer-duplicate.v1.price_changed', message, exchange='my-offers')
    await asyncio.sleep(1)

    # assert
    assert not await notification_center_stub.get_requests()
