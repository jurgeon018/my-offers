from datetime import datetime

import pytest
from cian_functional_test_utils.pytest_plugin import MockResponse


class TestMassOffersRestore:

    @pytest.mark.parametrize('status_tab, action_type, job_status', [
        ('notActive', 'all', 'Error'),
    ])
    async def test_restore_all(self, pg, http, status_tab, action_type, job_status, monolith_cian_announcementapi_mock):
        """ Проверяем восстановление всех объявлений """
        # arrange
        offer_id_1 = 11111111
        offer_id_2 = 22222222
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
                updated_at
            )
            VALUES
                ($1, $2, $3, $4, $5, $6),
                ($7, $8, $9, $10, $11, $12)
            """,
            [
                1, 123, user_id, master_user, now, now,
                2, 123, master_user, None, now, now,
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
                updated_at
            )
            VALUES
                ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15),
                ($16, $17, $18, $19, $20, $21, $22, $23, $24, $25, $26, $27, $28, $29, $30)
            """,
            [
                offer_id_1, master_user, master_user, 'sale', 'flat', status_tab, [], True, False, False, 'text', '{}',
                1, now, now,
                offer_id_2, master_user, user_id, 'sale', 'flat', status_tab, [], True, False, False, 'text', '{}', 1,
                now, now,
            ]
        )

        await monolith_cian_announcementapi_mock.add_stub(
            method='POST',
            path='/announcements-actions/v1/restore/',
            response=MockResponse(
                body={
                    'job_id': 123
                }
            ),
        )
        await monolith_cian_announcementapi_mock.add_stub(
            method='GET',
            path='/announcements-actions/v1/get-job-status/',
            response=[
                MockResponse(
                    body={
                        'state': 'InProgress',
                        'announcementsProgress': []
                    },
                    repeat=3
                ),
                MockResponse(
                    body={
                        'state': job_status,
                        'announcementsProgress': [
                            {'id': offer_id_1, 'state': 'Completed'},
                            {'id': offer_id_2, 'state': 'Error', 'error_message': 'Need more money!'},
                        ]
                    }
                ),
            ]
        )

        # act
        response = await http.request(
            'POST',
            '/public/v1/actions/restore-offers/',
            headers={
                'X-Real-UserId': master_user
            },
            json={
                'filters': {'status_tab': status_tab},
                'action_type': action_type
            },
        )

        # assert
        assert response.data == {
            'counters': {
                'draftCount': 0,
                'errorCount': 1,
                'restoredCount': 1,
                'xmlCount': 0
            },
            'total': 2,
            'offers': [
                {'message': None, 'offerId': offer_id_1, 'status': 'Completed'},
                {'message': 'Need more money!', 'offerId': offer_id_2, 'status': 'Error'},
            ]
        }

    @pytest.mark.parametrize('status_tab, action_type, job_status', [
        ('notActive', 'select', 'Error'),
    ])
    async def test_restore_selected(
            self,
            pg,
            http,
            status_tab,
            action_type,
            job_status,
            monolith_cian_announcementapi_mock
    ):
        """ Проверяем восстановление только выбранных объявлений """
        # arrange
        offer_id_1 = 11111111
        offer_id_2 = 22222222
        offer_id_3 = 33333333
        offer_id_4 = 44444444
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
                updated_at
            )
            VALUES
                ($1, $2, $3, $4, $5, $6),
                ($7, $8, $9, $10, $11, $12)
            """,
            [
                1, 123, user_id, master_user, now, now,
                2, 123, master_user, None, now, now,
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
                updated_at
            )
            VALUES
                ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15),
                ($16, $17, $18, $19, $20, $21, $22, $23, $24, $25, $26, $27, $28, $29, $30),
                ($31, $32, $33, $34, $35, $36, $37, $38, $39, $40, $41, $42, $43, $44, $45),
                ($46, $47, $48, $49, $50, $51, $52, $53, $54, $55, $56, $57, $58, $59, $60)
            """,
            [
                offer_id_1, master_user, master_user, 'sale', 'flat', status_tab, [], True, False, False, 'text',
                '{"id": %s}' % offer_id_1, 1, now, now,
                offer_id_2, master_user, master_user, 'sale', 'flat', status_tab, [], True, False, False, 'text',
                '{"id": %s}' % offer_id_2, 1, now, now,
                offer_id_3, master_user, user_id, 'sale', 'flat', status_tab, [], True, False, False, 'text',
                '{"id": %s}' % offer_id_3, 1, now, now,
                offer_id_4, master_user, user_id, 'sale', 'flat', status_tab, [], True, False, False, 'text',
                '{"id": %s, "status": "Draft"}' % offer_id_4, 1, now, now,
            ]
        )

        await monolith_cian_announcementapi_mock.add_stub(
            method='POST',
            path='/announcements-actions/v1/restore/',
            response=MockResponse(
                body={
                    'job_id': 123
                }
            ),
        )
        await monolith_cian_announcementapi_mock.add_stub(
            method='GET',
            path='/announcements-actions/v1/get-job-status/',
            response=[
                MockResponse(
                    body={
                        'state': 'InProgress',
                        'announcementsProgress': []
                    },
                    repeat=3,
                ),
                MockResponse(
                    body={
                        'state': job_status,
                        'announcementsProgress': [
                            {'id': offer_id_1, 'state': 'Completed'},
                            {'id': offer_id_3, 'state': 'Error', 'error_message': 'Need more money!'},
                        ]
                    }
                ),
            ]
        )

        # act
        response = await http.request(
            'POST',
            '/public/v1/actions/restore-offers/',
            headers={
                'X-Real-UserId': master_user
            },
            json={
                'filters': {'status_tab': status_tab},
                'offers_ids': [offer_id_1, offer_id_3, offer_id_4],
                'action_type': action_type
            },
        )

        # assert
        assert response.data == {
            'total': 3,
            'counters': {
                'draftCount': 1,
                'errorCount': 1,
                'restoredCount': 1,
                'xmlCount': 0
            },
            'offers': [
                {'message': None, 'offerId': offer_id_1, 'status': 'Completed'},
                {'message': 'Need more money!', 'offerId': offer_id_3, 'status': 'Error'},
            ]
        }

    @pytest.mark.parametrize('status_tab, action_type, job_status', [
        ('notActive', 'select', 'Error'),
    ])
    async def test_restore_selected__ignore_not_user_offers(
            self,
            pg,
            http,
            status_tab,
            action_type,
            job_status,
            monolith_cian_announcementapi_mock
    ):
        """ Проверяем восстановление только принадлежащих пользователю объявлений """
        # arrange
        offer_id_1 = 11111111
        strange_offer_id_2 = 22222222
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
                updated_at
            )
            VALUES
                ($1, $2, $3, $4, $5, $6),
                ($7, $8, $9, $10, $11, $12)
            """,
            [
                1, 123, user_id, master_user, now, now,
                2, 123, master_user, None, now, now,
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
                updated_at
            )
            VALUES
                ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15)
            """,
            [
                offer_id_1, master_user, master_user, 'sale', 'flat', status_tab, [], True, False, False, 'text',
                '{"id": %s}' % offer_id_1, 1, now, now,
            ]
        )

        await monolith_cian_announcementapi_mock.add_stub(
            method='POST',
            path='/announcements-actions/v1/restore/',
            response=MockResponse(
                body={
                    'job_id': 123
                }
            ),
        )
        await monolith_cian_announcementapi_mock.add_stub(
            method='GET',
            path='/announcements-actions/v1/get-job-status/',
            response=[
                MockResponse(
                    body={
                        'state': 'InProgress',
                        'announcementsProgress': []
                    },
                    repeat=3,
                ),
                MockResponse(
                    body={
                        'state': job_status,
                        'announcementsProgress': [
                            {'id': offer_id_1, 'state': 'Completed'},
                        ]
                    }
                ),
            ]
        )

        # act
        response = await http.request(
            'POST',
            '/public/v1/actions/restore-offers/',
            headers={
                'X-Real-UserId': master_user
            },
            json={
                'filters': {'status_tab': status_tab},
                'offers_ids': [offer_id_1, strange_offer_id_2],
                'action_type': action_type
            },
        )

        # assert
        assert response.data == {
            'total': 1,
            'counters': {
                'draftCount': 0,
                'errorCount': 0,
                'restoredCount': 1,
                'xmlCount': 0
            },
            'offers': [
                {'message': None, 'offerId': offer_id_1, 'status': 'Completed'},
            ]
        }

    @pytest.mark.parametrize('status_tab, action_type, job_status', [
        ('notActive', 'all', 'Error'),
    ])
    async def test_restore_selected__exclude_xml(
            self,
            pg,
            http,
            status_tab,
            action_type,
            job_status,
            monolith_cian_announcementapi_mock
    ):
        """ Проверяем восстановление всех объявлений, кроме XML """
        # arrange
        offer_id_1 = 11111111
        offer_id_2 = 22222222
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
                updated_at
            )
            VALUES
                ($1, $2, $3, $4, $5, $6),
                ($7, $8, $9, $10, $11, $12)
            """,
            [
                1, 123, user_id, master_user, now, now,
                2, 123, master_user, None, now, now,
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
                updated_at
            )
            VALUES
                ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15),
                ($16, $17, $18, $19, $20, $21, $22, $23, $24, $25, $26, $27, $28, $29, $30)
            """,
            [
                offer_id_1, master_user, master_user, 'sale', 'flat', status_tab, [], True, False, False, 'text', '{}',
                1, now, now,
                offer_id_2, master_user, user_id, 'sale', 'flat', status_tab, [], False, False, False, 'text',
                '{"id": 22222222, "source": "upload"}', 1,
                now, now,
            ]
        )

        await monolith_cian_announcementapi_mock.add_stub(
            method='POST',
            path='/announcements-actions/v1/restore/',
            response=MockResponse(
                body={
                    'job_id': 123
                }
            ),
        )
        await monolith_cian_announcementapi_mock.add_stub(
            method='GET',
            path='/announcements-actions/v1/get-job-status/',
            response=[
                MockResponse(
                    body={
                        'state': 'InProgress',
                        'announcementsProgress': []
                    },
                    repeat=3
                ),
                MockResponse(
                    body={
                        'state': job_status,
                        'announcementsProgress': [
                            {'id': offer_id_1, 'state': 'Completed'},
                        ]
                    }
                ),
            ]
        )

        # act
        response = await http.request(
            'POST',
            '/public/v1/actions/restore-offers/',
            headers={
                'X-Real-UserId': master_user
            },
            json={
                'filters': {'status_tab': status_tab},
                'action_type': action_type
            },
        )

        # assert
        assert response.data == {
            'total': 2,
            'counters': {
                'draftCount': 0,
                'errorCount': 0,
                'restoredCount': 1,
                'xmlCount': 1
            },
            'offers': [
                {'message': 'Нельзя автоматически восстановить XML', 'offerId': offer_id_2, 'status': 'Error'},
                {'message': None, 'offerId': offer_id_1, 'status': 'Completed'},
            ]
        }

    @pytest.mark.parametrize('status_tab, action_type, job_status', [
        ('notActive', 'select', 'Error'),
    ])
    async def test_restore_selected__bad_request(self, pg, http, status_tab, action_type, job_status):
        # arrange
        master_user = 333

        # act
        response = await http.request(
            'POST',
            '/public/v1/actions/restore-offers/',
            headers={
                'X-Real-UserId': master_user
            },
            json={
                'filters': {'status_tab': status_tab},
                'action_type': action_type,
                'offers_ids': []
            },
            expected_status=400
        )

        # assert
        assert response.data == {
            'message': 'offers_ids is empty with type `select`',
            'errors': [
                {'key': 'offersIds', 'code': 'offersIdsIsEmpty', 'message': 'offers_ids is empty with type `select`'}
            ]
        }
