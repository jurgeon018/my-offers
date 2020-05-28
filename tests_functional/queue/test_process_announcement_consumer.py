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
    # act
    await queue_service.wait_consumer('my-offers.process_announcement_v2')
    await queue_service.publish('announcement_reporting.change', offer, exchange='announcements')
    await asyncio.sleep(1)

    # assert
    row = await pg.fetchrow('SELECT * FROM offers ORDER BY offer_id DESC LIMIT 1')
    assert row['search_text'] == expected
