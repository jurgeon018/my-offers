import asyncio
from datetime import datetime

import pytest

from tests.utils import load_json_data


@pytest.mark.parametrize('offer', [
    load_json_data(__file__, 'announcement_similar.json')
])
async def test_duplicate_price_changed_producer__send_message_ok(queue_service, pg, offer, runtime_settings):
    # arrange
    await pg.execute(
        """
        INSERT INTO public.offers_similars_flat (
            offer_id,
            group_id,
            house_id,
            district_id,
            price,
            rooms_count,
            deal_type,
            sort_date,
            old_price
        )
        VALUES
            ($1, $2, $3, $4, $5, $6, $7, $8, $9)
        """,
        [
            236954116,
            None,
            None,
            341,
            4000000.0,
            2,
            'sale',
            datetime(2020, 9, 5),
            None,
        ]
    )
    await pg.execute('INSERT INTO offers_duplicates values(236954116, 173975523, \'2020-05-09\')')
    await runtime_settings.set({'SEND_PUSH_ON_DUPLICATE_PRICE_CHANGED': True})
    duplicate_queue = await queue_service.make_tmp_queue(
        routing_key='my-offers.offer-duplicate.v1.price_changed',
    )

    # act
    await queue_service.wait_consumer('my-offers.process_announcement_v2', timeout=15)
    await queue_service.publish('announcement_reporting.change', offer, exchange='announcements')

    # assert
    messages = await duplicate_queue.wait_messages(count=1, timeout=3)
    assert len(messages) == 1
    assert messages[0].routing_key == 'my-offers.offer-duplicate.v1.price_changed'
    assert messages[0].exchange == 'my-offers'
    assert messages[0].payload['duplicateOfferId'] == 236954116


@pytest.mark.parametrize('offer', [
    load_json_data(__file__, 'announcement_similar.json')
])
async def test_duplicate_price_changed_producer__is_not_duplicate__no_message(
        queue_service, pg, offer, runtime_settings
):
    # arrange
    await pg.execute(
        """
        INSERT INTO public.offers_similars_flat (
            offer_id,
            group_id,
            house_id,
            district_id,
            price,
            rooms_count,
            deal_type,
            sort_date,
            old_price
        )
        VALUES
            ($1, $2, $3, $4, $5, $6, $7, $8, $9)
        """,
        [
            236954116,
            None,
            None,
            341,
            4000000.0,
            2,
            'sale',
            datetime(2020, 9, 5),
            None,
        ]
    )
    await runtime_settings.set({'SEND_PUSH_ON_DUPLICATE_PRICE_CHANGED': True})
    duplicate_queue = await queue_service.make_tmp_queue(
        routing_key='my-offers.offer-duplicate.v1.price_changed',
    )

    # act
    await queue_service.wait_consumer('my-offers.process_announcement_v2', timeout=15)
    await queue_service.publish('announcement_reporting.change', offer, exchange='announcements')
    await asyncio.sleep(3)

    # assert
    messages = await duplicate_queue.get_messages()
    assert len(messages) == 0


@pytest.mark.parametrize('offer', [
    load_json_data(__file__, 'announcement_similar.json')
])
async def test_duplicate_price_changed_producer__price_didnot_change__no_message(
        queue_service, pg, offer, runtime_settings
):
    # arrange
    await pg.execute(
        """
        INSERT INTO public.offers_similars_flat (
            offer_id,
            group_id,
            house_id,
            district_id,
            price,
            rooms_count,
            deal_type,
            sort_date,
            old_price
        )
        VALUES
            ($1, $2, $3, $4, $5, $6, $7, $8, $9)
        """,
        [
            236954116,
            None,
            None,
            341,
            4539000.0,
            2,
            'sale',
            datetime(2020, 9, 5),
            None,
        ]
    )
    await pg.execute('INSERT INTO offers_duplicates values(236954116, 173975523, \'2020-05-09\')')
    await runtime_settings.set({'SEND_PUSH_ON_DUPLICATE_PRICE_CHANGED': True})
    duplicate_queue = await queue_service.make_tmp_queue(
        routing_key='my-offers.offer-duplicate.v1.price_changed',
    )

    # act
    await queue_service.wait_consumer('my-offers.process_announcement_v2', timeout=15)
    await queue_service.publish('announcement_reporting.change', offer, exchange='announcements')
    await asyncio.sleep(3)

    # assert
    messages = await duplicate_queue.get_messages()
    assert len(messages) == 0


@pytest.mark.parametrize('offer', [
    load_json_data(__file__, 'announcement_similar.json')
])
async def test_duplicate_price_changed_producer__rs_off__no_message(queue_service, pg, offer, runtime_settings):
    # arrange
    await pg.execute(
        """
        INSERT INTO public.offers_similars_flat (
            offer_id,
            group_id,
            house_id,
            district_id,
            price,
            rooms_count,
            deal_type,
            sort_date,
            old_price
        )
        VALUES
            ($1, $2, $3, $4, $5, $6, $7, $8, $9)
        """,
        [
            236954116,
            None,
            None,
            341,
            4000000.0,
            2,
            'sale',
            datetime(2020, 9, 5),
            None,
        ]
    )
    await pg.execute('INSERT INTO offers_duplicates values(236954116, 173975523, \'2020-05-09\')')
    await runtime_settings.set({'SEND_PUSH_ON_DUPLICATE_PRICE_CHANGED': False})
    duplicate_queue = await queue_service.make_tmp_queue(
        routing_key='my-offers.offer-duplicate.v1.price_changed',
    )

    # act
    await queue_service.wait_consumer('my-offers.process_announcement_v2', timeout=15)
    await queue_service.publish('announcement_reporting.change', offer, exchange='announcements')
    await asyncio.sleep(3)

    # assert
    messages = await duplicate_queue.get_messages()
    assert len(messages) == 0
