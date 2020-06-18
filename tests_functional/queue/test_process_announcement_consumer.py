import asyncio

import pytest

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
    Сохрарнение активного объявления.
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
    Сохрарнение архивного объявления.
    """
    # act
    await queue_service.wait_consumer('my-offers.process_announcement_v2')
    await queue_service.publish('announcement_reporting.change', offer_archive, exchange='announcements')
    await asyncio.sleep(1)

    # assert
    row = await pg.fetchrow('SELECT * FROM offers ORDER BY offer_id DESC LIMIT 1')

    assert row['status_tab'] == 'archived'
    assert row['row_version'] == -1


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
    """
    # act
    await queue_service.wait_consumer('my-offers.process_announcement_v2')
    await queue_service.publish('announcement_reporting.change', offer_active, exchange='announcements')
    await queue_service.publish('announcement_reporting.change', offer_archive, exchange='announcements')
    await asyncio.sleep(1)

    # assert
    row = await pg.fetchrow('SELECT * FROM offers ORDER BY offer_id DESC LIMIT 1')

    assert row['status_tab'] == 'archived'
    assert row['row_version'] == -1


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
    """
    # act
    await queue_service.wait_consumer('my-offers.process_announcement_v2')
    await queue_service.publish('announcement_reporting.change', offer_archive, exchange='announcements')
    await queue_service.publish('announcement_reporting.change', offer_active, exchange='announcements')
    await asyncio.sleep(1)

    # assert
    row = await pg.fetchrow('SELECT * FROM offers ORDER BY offer_id DESC LIMIT 1')

    assert row['status_tab'] == 'active'
    assert row['row_version'] == 31146468040
