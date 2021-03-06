import json
from datetime import datetime
from pathlib import Path

import pytest
import pytz


async def test_v2_get_offers_public__not_found__200(http):
    # act
    response = await http.request(
        'POST',
        '/public/v2/get-offers/',
        json={
            'filters': {
                'statusTab': 'active',
                'searchText': '+7 (929) 444 55-77 Москва'
            }
        },
        headers={
            'X-Real-UserId': 13933440
        },
    )

    # assert
    assert len(response.data['offers']) == 0


async def test_v2_get_offers_public__search_text__result(http, pg):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers.sql')

    # act
    response = await http.request(
        'POST',
        '/public/v2/get-offers/',
        json={
            'filters': {
                'statusTab': 'active',
                'searchText': '+7 (962) 078 83-57 Красноярский край'
            }
        },
        headers={
            'X-Real-UserId': 29437831
        },
    )

    # assert
    assert response.data['offers'][0]['id'] == 209194477


@pytest.mark.parametrize('x_real_user, can_change_publisher', [
    (333, True),
    (222, False),
])
async def test_v2_get_offers_public__can_change_publisher(http, pg, x_real_user, can_change_publisher):
    # arrange
    offer_id_1 = 11111111
    user_id = 222
    master_user = 333

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
            1, 123, user_id, master_user, now, now, 'Specialist',
            2, 123, master_user, None, now, now, 'Agency'
        ]
    )

    offer_json = json.dumps({
        'id': offer_id_1,
        'status': 'Published',
        'category': 'flatRent',
        'bargainTerms': {
            'currency': 'rur'
        }
    })

    await pg.execute(
        """
        INSERT INTO public.offers (
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
            offer_id_1, master_user, user_id, 'sale', 'flat', 'active', [], True, False, False, 'text',
            offer_json, 1, now, now,
        ]
    )

    # act
    response = await http.request(
        'POST',
        '/public/v2/get-offers/',
        json={
            'filters': {
                'statusTab': 'active',
            }
        },
        headers={
            'X-Real-UserId': x_real_user
        },
    )

    # assert
    assert response.data['offers'][0]['id'] == 11111111
    assert response.data['offers'][0]['availableActions']['canChangePublisher'] is can_change_publisher


@pytest.mark.parametrize('x_real_user, can_raise_without_addform, expected_offer_id, settings', [
    # запрещено всем
    (444, False, 22222222, []),
    (333, False, 11111111, []),
    (222, False, 11111111, []),
    # разрешено мастерам
    (444, False, 22222222, ['master_agent']),
    (333, True, 11111111, ['master_agent']),
    (222, False, 11111111, ['master_agent']),
    # разрешено сабам
    (444, False, 22222222, ['sub_agent']),
    (333, False, 11111111, ['sub_agent']),
    (222, True, 11111111, ['sub_agent']),
    # разрешено агентам без иерархии
    (444, True, 22222222, ['agent']),
    (333, False, 11111111, ['agent']),
    (222, False, 11111111, ['agent']),
])
async def test_v2_get_offers_public__can_raise_without_addform(
        http,
        pg,
        runtime_settings,
        x_real_user,
        can_raise_without_addform,
        settings,
        expected_offer_id,
):
    # arrange
    offer_id_1 = 11111111
    offer_id_2 = 22222222
    user_id = 222
    user_id_2 = 444
    master_user = 333

    await runtime_settings.set({'CAN_RAISE_WITHOUT_ADDFORM': settings})

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
            ($8, $9, $10, $11, $12, $13, $14),
            ($15, $16, $17, $18, $19, $20, $21)
        """,
        [
            1, 123, user_id, master_user, now, now, 'Specialist',
            2, 123, master_user, None, now, now, 'Agency',
            3, 123, user_id_2, None, now, now, 'Agency',
        ]
    )

    offer_json_1 = json.dumps({
        'id': offer_id_1,
        'status': 'Published',
        'category': 'flatRent',
        'bargainTerms': {
            'currency': 'rur'
        }
    })
    offer_json_2 = json.dumps({
        'id': offer_id_2,
        'status': 'Published',
        'category': 'flatRent',
        'bargainTerms': {
            'currency': 'rur'
        }
    })

    await pg.execute(
        """
        INSERT INTO public.offers (
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
            ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15),
            ($16, $17, $18, $19, $20, $21, $22, $23, $24, $25, $26, $27, $28, $29, $30)
        """,
        [
            offer_id_1, master_user, user_id, 'sale', 'flat', 'active', [], True, False, False, 'text',
            offer_json_1, 1, now, now,
            offer_id_2, user_id_2, user_id_2, 'sale', 'flat', 'active', [], True, False, False, 'text',
            offer_json_2, 1, now, now,
        ]
    )

    # act
    response = await http.request(
        'POST',
        '/public/v2/get-offers/',
        json={
            'filters': {
                'statusTab': 'active',
            }
        },
        headers={
            'X-Real-UserId': x_real_user
        },
    )

    # assert
    assert response.data['offers'][0]['id'] == expected_offer_id
    assert response.data['offers'][0]['availableActions']['canRaiseWithoutAddform'] is can_raise_without_addform


async def test_v2_get_offers_public__can_view_similar_offers(http, pg):
    # arrange
    offer_id_1 = 11111111
    user_id = 222
    master_user = 333
    now = datetime.now()

    await pg.execute(
        """
        INSERT INTO agents_hierarchy (
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
            1, 123, user_id, master_user, now, now, 'Specialist',
            2, 123, master_user, None, now, now, 'Agency'
        ]
    )

    offer_json = json.dumps({
        'id': offer_id_1,
        'status': 'Published',
        'category': 'flatRent',
        'bargainTerms': {
            'currency': 'rur'
        }
    })

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
            updated_at,
            is_test
        )
        VALUES
            ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16)
        """,
        [
            offer_id_1, master_user, user_id, 'sale', 'flat', 'active', [], True, False, False, 'text',
            offer_json, 1, now, now, False
        ]
    )

    await pg.execute(
        'INSERT INTO offers_similars_flat(offer_id, deal_type, sort_date, group_id, house_id, price, rooms_count, '
        'publisher_user_id) '
        'VALUES(11111111, \'sale\', \'2020-08-10\', 11111111, 123, 10990000, 4, 1)'
    )
    await pg.execute(
        'INSERT INTO offers_similars_flat(offer_id, deal_type, sort_date, group_id, publisher_user_id) '
        'VALUES(231659418, \'sale\', \'2020-08-10\', 11111111, 1)'
    )
    await pg.execute(
        'INSERT INTO offers_similars_flat(offer_id, deal_type, sort_date, group_id, publisher_user_id) '
        'VALUES(173975523, \'sale\', \'2020-08-10\', 11111111, 1)'
    )
    await pg.execute(
        'INSERT INTO offers_similars_flat(offer_id, deal_type, sort_date, group_id, house_id, price, rooms_count, '
        'publisher_user_id) '
        'VALUES(22222222, \'sale\', \'2020-08-10\', 22222222, 123, 10990000, 4, 1)'
    )

    # act
    response = await http.request(
        'POST',
        '/public/v2/get-offers/',
        json={
            'filters': {
                'statusTab': 'active',
            }
        },
        headers={
            'X-Real-UserId': master_user
        },
    )

    # assert
    assert response.data['offers'][0]['id'] == offer_id_1
    assert response.data['offers'][0]['availableActions']['canViewSimilarOffers'] is True
    assert response.data['offers'][0]['availableActions']['canRaise'] is True
    assert response.data['offers'][0]['pageSpecificInfo']['activeInfo']['duplicatesCount'] == 2
    assert response.data['offers'][0]['pageSpecificInfo']['activeInfo']['sameBuildingCount'] == 1


@pytest.mark.parametrize('payed_by, expected_ids', (
    ('byMaster', [1, 2]),
    ('byAgent', [3]),
    ('any', [1, 2, 3, 4]),
))
async def test_get_active_offers_by_payed_by(pg, http, payed_by, expected_ids):
    # arrange
    now = datetime.now()
    user_id = 2
    master_user_id = 3
    offers_raw_data = {
        id: json.dumps({
                'id': id,
                'status': 'Published',
                'category': 'flatRent',
                'bargainTerms': {
                    'currency': 'rur'
                }
            })
        for id in [1, 2, 3, 4, 5]
    }

    await pg.execute(
        """
        INSERT INTO public.agents_hierarchy (
            id,
            row_version,
            realty_user_id,
            master_agent_user_id,
            created_at,
            updated_at
        )
        VALUES
            ($1, $2, $3, $4, $5, $6),
            ($7, $8, $9, $10, $11, $12)
        """,
        [
            1, 1, user_id, master_user_id, now, now,
            2, 1, master_user_id, None, now, now,
        ]
    )
    await pg.execute(
        """
        INSERT INTO public.offers (
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
            updated_at,
            payed_by
        )
        VALUES
            ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16),
            ($17, $18, $19, $20, $21, $22, $23, $24, $25, $26, $27, $28, $29, $30, $31, $32),
            ($33, $34, $35, $36, $37, $38, $39, $40, $41, $42, $43, $44, $45, $46, $47, $48),
            ($49, $50, $51, $52, $53, $54, $55, $56, $57, $58, $59, $60, $61, $62, $63, $64),
            ($65, $66, $67, $68, $69, $70, $71, $72, $73, $74, $75, $76, $77, $78, $79, $80)
        """,
        [
            1, master_user_id, user_id, 'sale', 'flat', 'active', [], True, False, False, 'text',
            offers_raw_data.get(1), 1, now, now, master_user_id,
            2, master_user_id, master_user_id, 'sale', 'flat', 'active', [], True, False, False, 'text',
            offers_raw_data.get(2), 1, now, now, master_user_id,
            3, master_user_id, user_id, 'sale', 'flat', 'active', [], True, False, False, 'text',
            offers_raw_data.get(3), 1, now, now, user_id,
            4, master_user_id, user_id, 'sale', 'flat', 'active', [], True, False, False, 'text',
            offers_raw_data.get(4), 1, now, now, None,
            5, master_user_id, user_id, 'sale', 'flat', 'deleted', [], True, False, False, 'text',
            offers_raw_data.get(5), 1, now, now, None
        ]
    )

    # act
    response = await http.request(
        'POST',
        '/public/v2/get-offers/',
        json={
            'filters': {
                'statusTab': 'active',
                'payedBy': payed_by
            }
        },
        headers={
            'X-Real-UserId': master_user_id
        },
    )

    # assert
    assert {offer['id'] for offer in response.data['offers']} == set(expected_ids)


async def test_get_active_offers_payed_by_labels(pg, http):
    # arrange
    now = datetime.now()
    user_id = 2
    master_user_id = 3
    offers_raw_data = {
        id: json.dumps({
                'id': id,
                'status': 'Published',
                'category': 'flatRent',
                'bargainTerms': {
                    'currency': 'rur'
                }
            })
        for id in [1, 2, 3, 4]
    }

    await pg.execute(
        """
        INSERT INTO public.agents_hierarchy (
            id,
            row_version,
            realty_user_id,
            master_agent_user_id,
            created_at,
            updated_at
        )
        VALUES
            ($1, $2, $3, $4, $5, $6),
            ($7, $8, $9, $10, $11, $12)
        """,
        [
            1, 1, user_id, master_user_id, now, now,
            2, 1, master_user_id, None, now, now,
        ]
    )
    await pg.execute(
        """
        INSERT INTO public.offers (
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
            updated_at,
            payed_by
        )
        VALUES
            ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16),
            ($17, $18, $19, $20, $21, $22, $23, $24, $25, $26, $27, $28, $29, $30, $31, $32),
            ($33, $34, $35, $36, $37, $38, $39, $40, $41, $42, $43, $44, $45, $46, $47, $48),
            ($49, $50, $51, $52, $53, $54, $55, $56, $57, $58, $59, $60, $61, $62, $63, $64)
        """,
        [
            1, master_user_id, user_id, 'sale', 'flat', 'active', [], True, False, False, 'text',
            offers_raw_data.get(1), 1, now, now, master_user_id,
            2, master_user_id, user_id, 'sale', 'flat', 'active', [], True, False, False, 'text',
            offers_raw_data.get(2), 1, now, now, user_id,
            3, master_user_id, user_id, 'sale', 'flat', 'active', [], True, False, False, 'text',
            offers_raw_data.get(3), 1, now, now, None,
            4, master_user_id, user_id, 'sale', 'flat', 'deleted', [], True, False, False, 'text',
            offers_raw_data.get(4), 1, now, now, None
        ]
    )

    # act
    response = await http.request(
        'POST',
        '/public/v2/get-offers/',
        json={
            'filters': {
                'statusTab': 'active',
            }
        },
        headers={
            'X-Real-UserId': master_user_id
        },
    )

    # assert
    assert {offer['id']: offer['payedBy'] for offer in response.data['offers']} == {
        1: 'byMaster',
        2: 'byAgent',
        3: None,
    }


async def test_get_active_offers_with_relevance_warnings(pg, http):
    # arrange
    now = datetime(2020, 4, 20, 12, tzinfo=pytz.UTC)

    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers_similar.sql')
    await pg.execute(
        """
        INSERT INTO offer_relevance_warnings (
            offer_id,
            check_id,
            active,
            due_date,
            created_at,
            updated_at
        )
        VALUES
            ($1,  $2,  $3,  $4,  $5,  $6),
            ($7,  $8,  $9,  $10, $11, $12),
            ($13, $14, $15, $16, $17, $18)
        """,
        [
            162730477, '0A838C51-583B-4346-BDC6-E24AC8CAE3A4', True, None, now, now,
            162729892, '11D8C8C2-41B1-4EE5-A2F0-41F4CB22EA1C', True, now, now, now,
            162730289, '7DF35154-E8B3-47C0-977A-8D4137C9C1DA', False, now, now, now,
        ]
    )

    # act
    response = await http.request(
        'POST',
        '/public/v2/get-offers/',
        json={
            'filters': {
                'statusTab': 'active',
                'hasRelevanceWarning': True,
            }
        },
        headers={
            'X-Real-UserId': 8088578,
        },
    )

    # assert
    assert {offer['id']: offer['pageSpecificInfo']['activeInfo']['relevance'] for offer in response.data['offers']} == {
        162730477: {
            'checkId': '0A838C51-583B-4346-BDC6-E24AC8CAE3A4',
            'warningMessage': (
                'Если объявление актуально, подтвердите это. Если неактуально, вы можете перенести его в архив.'
            ),
        },
        162729892: {
            'checkId': '11D8C8C2-41B1-4EE5-A2F0-41F4CB22EA1C',
            'warningMessage': (
                'Допустимый срок публикации истекает 20 апреля 2020 года, затем объявление будет автоматически '
                'снято с публикации. Если объявление актуально, подтвердите это. Если неактуально, вы можете '
                'перенести его в архив.'
            ),
        },
    }


async def test_v2_get_offers_public__sort_by_declined_date__sorted_offers_by_declined_date(http, pg):
    # arrange
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers_for_sort.sql')

    # act
    response = await http.request(
        'POST',
        '/public/v2/get-offers/',
        json={
            'filters': {
                'statusTab': 'declined',
            },
            'sort': 'declinedDate'
        },
        headers={
            'X-Real-UserId': 29437839
        },
    )

    # assert
    assert [o['id'] for o in response.data['offers']] == [209194482, 209194480, 209194481]


async def test_v2_get_offers_public__get_archived_removed_by_moderator__can_delete_offer(http, pg):
    # arrange
    expected = {
        'canChangePublisher': False,
        'canDelete': True,
        'canEdit': False,
        'canMoveToArchive': False,
        'canRaise': False,
        'canRaiseWithoutAddform': False,
        'canRestore': False,
        'canUpdateEditDate': False,
        'canViewSimilarOffers': False
    }
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers_for_available_actions.sql')

    # act
    response = await http.request(
        'POST',
        '/public/v2/get-offers/',
        headers={
            'X-Real-UserId': 27864412
        },
        json={
            'filters': {
                'statusTab': 'archived'
            }
        },
    )
    assert response.data['offers'][0]['availableActions'] == expected


async def test_v2_get_offers_public__get_declined_removed_by_moderator__cant_delete_offer(http, pg):
    # arrange
    expected = {
        'canChangePublisher': False,
        'canDelete': False,
        'canEdit': False,
        'canMoveToArchive': False,
        'canRaise': False,
        'canRaiseWithoutAddform': False,
        'canRestore': False,
        'canUpdateEditDate': False,
        'canViewSimilarOffers': False
    }
    await pg.execute_scripts(Path('tests_functional') / 'data' / 'offers_for_available_actions.sql')

    # act
    response = await http.request(
        'POST',
        '/public/v2/get-offers/',
        headers={
            'X-Real-UserId': 27864413
        },
        json={
            'filters': {
                'statusTab': 'declined'
            }
        },
    )
    assert response.data['offers'][0]['availableActions'] == expected
