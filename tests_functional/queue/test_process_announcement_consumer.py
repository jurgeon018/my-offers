import asyncio
from copy import deepcopy
from datetime import datetime, timedelta

import pytest
from cian_json import json

from tests_functional.utils import load_json_data


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ('offer', 'expected'),
    (
        (
            load_json_data(__file__, 'announcement.json'),
            '228433597 4951348421 4951274372 ул. Лобачевского, вл. 120, корп. 1 Москва '
            'улица Лобачевского 120 д120 д 120 120д Аминьевское шоссе Мичуринский '
            'проспект Раменки метро ЗАО Раменки район Матвеевская Матвеевская Очаково I '
            'Очаково I Кунцево I Кунцево I станиция Крылья ЖК жилой комплекс 1-комн.\xa0кв., '
            '68\xa0м², 6/39\xa0этаж 1 комн комнатная 6 39 Продается однокомнатная квартира  98 '
            'в новостройке'
        ),
        (
            load_json_data(__file__, 'announcement_empty_address.json'),
            '228433597 4951348421 4951274372 ул. Лобачевского, вл. 120, корп. 1 '
            'Аминьевское шоссе Мичуринский проспект Раменки метро ЗАО Раменки район '
            'Матвеевская Матвеевская Очаково I Очаково I Кунцево I Кунцево I станиция '
            'Крылья ЖК жилой комплекс 1-комн.\xa0кв., 68\xa0м², 6/39\xa0этаж 1 комн комнатная 6 39 '
            'Продается однокомнатная квартира  98 в новостройке'
        ),
    ),
)
async def test_process_announcement_consumer(queue_service, pg, offer, expected):
    """
    Сохранение активного объявления.
    """
    # act
    await queue_service.wait_consumer('my-offers.process_announcement_v2')
    await queue_service.publish('announcement_reporting.change', offer, exchange='announcements')
    await asyncio.sleep(1)

    # assert
    row = await pg.fetchrow('SELECT * FROM offers ORDER BY offer_id DESC LIMIT 1')
    assert row['search_text'] == expected


@pytest.mark.asyncio
@pytest.mark.parametrize('offer_archive', [
    load_json_data(__file__, 'announcement_archive.json')
])
async def test_process_announcement_consumer__archive_offer(queue_service, pg, offer_archive):
    """
    Сохранение архивного объявления.
    """
    # act
    await queue_service.wait_consumer('my-offers.process_announcement_v2')
    await queue_service.publish('announcement_reporting.change', offer_archive, exchange='announcements')
    await asyncio.sleep(1)

    # assert
    row = await pg.fetchrow('SELECT * FROM offers ORDER BY offer_id DESC LIMIT 1')

    assert row['status_tab'] == 'archived'
    assert row['row_version'] == 1


@pytest.mark.asyncio
@pytest.mark.parametrize('offer_archive, offer_active', [
    (
        load_json_data(__file__, 'announcement_archive.json'),
        load_json_data(__file__, 'announcement.json')
    )
])
async def test_process_announcement_consumer__archive_offer_after_active_offer(
        queue_service,
        pg,
        offer_archive,
        offer_active
):
    """
    Сохрарнение архивного объявления после активного объявления.
    Дата архивного события больше активного.
    """
    # arrange
    offer_active['date'] = str(datetime(2020, 1, 1))
    offer_active['model']['rowVersion'] = 123
    offer_archive['date'] = str(datetime.now() + timedelta(days=5))
    offer_archive['model']['rowVersion'] = 1

    # act
    await queue_service.wait_consumer('my-offers.process_announcement_v2')
    await queue_service.publish('announcement_reporting.change', offer_active, exchange='announcements')
    await queue_service.publish('announcement_reporting.change', offer_archive, exchange='announcements')
    await asyncio.sleep(1)

    # assert
    row = await pg.fetchrow('SELECT * FROM offers ORDER BY offer_id DESC LIMIT 1')

    assert row['status_tab'] == 'archived'
    assert row['row_version'] == 123


@pytest.mark.asyncio
@pytest.mark.parametrize('offer_archive, offer_active', [
    (
        load_json_data(__file__, 'announcement_archive.json'),
        load_json_data(__file__, 'announcement.json')
    )
])
async def test_process_announcement_consumer__active_offer_after_archive_offer(
        queue_service,
        pg,
        offer_archive,
        offer_active
):
    """
    Сохрарнение активного объявления после архивного объявления.
    Дата активного меньше даты архивного.
    """
    offer_archive['date'] = str(datetime.now() + timedelta(days=5))
    offer_archive['model']['rowVersion'] = 123
    offer_active['date'] = str(datetime(2020, 1, 1))
    offer_active['model']['rowVersion'] = 122

    # act
    await queue_service.wait_consumer('my-offers.process_announcement_v2')
    await queue_service.publish('announcement_reporting.change', offer_archive, exchange='announcements')
    await queue_service.publish('announcement_reporting.change', offer_active, exchange='announcements')
    await asyncio.sleep(1)

    # assert
    row = await pg.fetchrow('SELECT * FROM offers ORDER BY offer_id DESC LIMIT 1')

    assert row['status_tab'] == 'archived'
    assert row['row_version'] == 123


@pytest.mark.asyncio
@pytest.mark.parametrize('offer', [
    load_json_data(__file__, 'announcement_codegen.json')
])
async def test_process_announcement_consumer__codegen_fix_validate(queue_service, pg, offer):
    # act
    await queue_service.wait_consumer('my-offers.process_announcement_v2')
    await queue_service.publish('announcement_reporting.change', offer, exchange='announcements')
    await asyncio.sleep(1)

    # assert
    row = await pg.fetchrow('SELECT * FROM offers ORDER BY offer_id DESC LIMIT 1')
    raw_data = json.loads(row['raw_data'])

    assert raw_data['phones'] == [None]
    assert raw_data['bargainTerms'].get('price') is None


@pytest.mark.asyncio
@pytest.mark.parametrize('offer_active', [
    load_json_data(__file__, 'announcement.json')
])
async def test_process_announcement_consumer__row_version_increment(
        queue_service,
        pg,
        offer_active
):
    """
    Сохрарнение активного объявления c row_version=2 после активного объявления row_version=1.
    """

    offer_active_1 = deepcopy(offer_active)
    offer_active_1['model']['rowVersion'] = 1
    offer_active_1['date'] = str(datetime.now())

    offer_active_2 = deepcopy(offer_active)
    offer_active_2['model']['rowVersion'] = 2
    offer_active_2['date'] = str(datetime.now() + timedelta(seconds=10))

    # act
    await queue_service.wait_consumer('my-offers.process_announcement_v2')
    await queue_service.publish('announcement_reporting.change', offer_active_1, exchange='announcements')
    await asyncio.sleep(.5)
    await queue_service.publish('announcement_reporting.change', offer_active_2, exchange='announcements')
    await asyncio.sleep(1)

    # assert
    row = await pg.fetchrow('SELECT * FROM offers ORDER BY offer_id DESC LIMIT 1')

    assert row['status_tab'] == 'active'
    assert row['row_version'] == 2


@pytest.mark.asyncio
@pytest.mark.parametrize('offer_active', [
    load_json_data(__file__, 'announcement.json')
])
async def test_process_announcement_consumer__offer_not_updated_with_old_row_version(
        queue_service,
        pg,
        offer_active
):
    """
    Сохрарнение активного объявления c row_version=1 после активного объявления row_version=2.
    """

    offer_active_1 = deepcopy(offer_active)
    offer_active_1['model']['rowVersion'] = 2
    offer_active_1['date'] = str(datetime.now() + timedelta(seconds=10))

    offer_active_2 = deepcopy(offer_active)
    offer_active_2['model']['rowVersion'] = 1
    offer_active_2['date'] = str(datetime.now())

    # act
    await queue_service.wait_consumer('my-offers.process_announcement_v2')
    await queue_service.publish('announcement_reporting.change', offer_active_1, exchange='announcements')
    await asyncio.sleep(.5)
    await queue_service.publish('announcement_reporting.change', offer_active_2, exchange='announcements')
    await asyncio.sleep(1)

    # assert
    row = await pg.fetchrow('SELECT * FROM offers ORDER BY offer_id DESC LIMIT 1')

    assert row['status_tab'] == 'active'
    assert row['row_version'] == 2


@pytest.mark.asyncio
@pytest.mark.parametrize('offer_archive, offer_active', [
    (
        load_json_data(__file__, 'announcement_archive.json'),
        load_json_data(__file__, 'announcement.json')
    )
])
async def test_process_announcement_consumer__archive_updated_to_active(
        queue_service,
        pg,
        offer_archive,
        offer_active
):
    """
    Сохранение активного объявления после архивного объявления.
    Архивное объявление обновлено до активного.
    """
    archive_row_version = 0
    offer_archive['date'] = str(datetime.now())
    offer_archive['model']['rowVersion'] = archive_row_version

    active_row_version = 111
    offer_active['date'] = str(datetime.now() + timedelta(days=5))
    offer_active['model']['rowVersion'] = active_row_version

    # act
    await queue_service.wait_consumer('my-offers.process_announcement_v2')
    await queue_service.publish('announcement_reporting.change', offer_archive, exchange='announcements')
    await asyncio.sleep(.5)
    await queue_service.publish('announcement_reporting.change', offer_active, exchange='announcements')
    await asyncio.sleep(1)

    # assert
    row = await pg.fetchrow('SELECT * FROM offers ORDER BY offer_id DESC LIMIT 1')

    assert row['status_tab'] == 'active'
    assert row['row_version'] == active_row_version


@pytest.mark.asyncio
@pytest.mark.parametrize(('offer', 'master_user_id', 'published_user_id', 'publisher_user_id', 'offer_id', 'expected'), [
    (load_json_data(__file__, 'announcement.json'),
     1, 2, 1, 1, 1),
    (load_json_data(__file__, 'announcement.json'),
     1, 2, 2, 1, 2),
])
async def test_process_announcement_consumer__payed_by(
        queue_service,
        pg,
        offer,
        master_user_id,
        published_user_id,
        publisher_user_id,
        offer_id,
        expected
):
    """
    Проверка проставления корректного значения в поле payed_by
    в зависимости от пришедших в сообщении идентификаторов.
    """
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
            updated_at,
            account_type
        )
        VALUES
            ($1, $2, $3, $4, $5, $6, $7),
            ($8, $9, $10, $11, $12, $13, $14)
        """,
        [
            1, 1, published_user_id, master_user_id, now, now, 'Specialist',
            2, 1, master_user_id, None, now, now, 'Agency'
        ]
    )
    await asyncio.sleep(1)

    # arrange
    await pg.execute(
        """
        INSERT INTO public.offers_billing_contracts (
            id,
            user_id,
            actor_user_id,
            publisher_user_id,
            offer_id,
            start_date,
            payed_till,
            row_version,
            is_deleted,
            created_at,
            updated_at
        )
        VALUES
            ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
        """,
        [
            1, 1, 1, publisher_user_id, offer_id, now, now, 1, False, now, now
        ]
    )
    await asyncio.sleep(1)

    offer['model']['publishedUserId'] = published_user_id
    offer['model']['userId'] = published_user_id
    offer['model']['id'] = offer_id

    # act
    await queue_service.wait_consumer('my-offers.process_announcement_v2')
    await queue_service.publish('announcement_reporting.change', offer, exchange='announcements')
    await asyncio.sleep(1)

    # assert
    row = await pg.fetchrow('SELECT * FROM offers ORDER BY offer_id DESC LIMIT 1')

    assert row['payed_by'] == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(('offer', 'published_user_id', 'expected'), [
    (load_json_data(__file__, 'announcement.json'), 1, None),
])
async def test_process_announcement_consumer__payed_by_without_master(
        queue_service,
        pg,
        offer,
        published_user_id,
        expected
):
    """
    Проверка проставления корректного значения в поле payed_by
    в случае учетной записи без мастера.
    """
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
            updated_at,
            account_type
        )
        VALUES
            ($1, $2, $3, $4, $5, $6, $7)
        """,
        [
            1, 1, published_user_id, None, now, now, 'Specialist',
        ]
    )

    offer['model']['publishedUserId'] = published_user_id
    offer['model']['userId'] = published_user_id

    # act
    await queue_service.wait_consumer('my-offers.process_announcement_v2')
    await queue_service.publish('announcement_reporting.change', offer, exchange='announcements')
    await asyncio.sleep(1)

    # assert
    row = await pg.fetchrow('SELECT * FROM offers ORDER BY offer_id DESC LIMIT 1')

    assert row['payed_by'] == expected


@pytest.mark.asyncio
@pytest.mark.parametrize(('offer', 'expected'), [
    (load_json_data(__file__, 'announcement.json'), None),
])
async def test_process_announcement_consumer__payed_by_missing_billing(
        queue_service,
        pg,
        offer,
        expected
):
    """
    При отсутствующей записи объявления в таблице биллинга
    в поле payed_by записывается пустое значение.
    """
    # act
    await queue_service.wait_consumer('my-offers.process_announcement_v2')
    await queue_service.publish('announcement_reporting.change', offer, exchange='announcements')
    await asyncio.sleep(1)

    # assert
    row = await pg.fetchrow('SELECT * FROM offers ORDER BY offer_id DESC LIMIT 1')

    assert row['payed_by'] == expected
