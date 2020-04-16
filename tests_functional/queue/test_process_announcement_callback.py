import asyncio

import pytest

from tests_functional.utils import load_json_data


@pytest.mark.asyncio
async def test_process_announcement_consumer(queue_service, pg):
    # act
    await queue_service.wait_consumer('my-offers.process_announcement_v2')
    data = load_json_data(__file__, 'announcement.json')
    search_text = '228433597 4951348421 4951274372 ул. Лобачевского, вл. 120, корп. 1 Москва Лобачевского 120 д120 д ' \
                  '120 120д Аминьевское шоссе Мичуринский проспект Раменки ЗАО Раменки Матвеевская Матвеевская ' \
                  'Очаково I Очаково I Кунцево I Кунцево I Крылья 1-комн. кв., 68 м², 6/39 этаж 6 39 Продается ' \
                  'однокомнатная квартира  98 в новостройке'
    await queue_service.publish('announcement_reporting.change', data, exchange='announcements')
    await asyncio.sleep(0.5)

    # assert
    row = await pg.fetchrow('SELECT * FROM offers WHERE offer_id = $1', [228433597])
    assert row['search_text'] == search_text
