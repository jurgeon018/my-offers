from datetime import datetime

import pytest
from cian_functional_test_utils.pytest_plugin import MockResponse


@pytest.mark.skip  # TODO: remove
class TestMassOffersRestore:

    @pytest.mark.parametrize('status_tab, action_type, job_status', [
        ('notActive', 'all', 'Error'),
        ('active', 'all', 'Completed'),
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
                offer_id_2, user_id, master_user, 'sale', 'flat', status_tab, [], True, False, False, 'text', '{}', 1,
                now, now,
            ]
        )

        await monolith_cian_announcementapi_mock.add_stub(
            method='POST',
            path='/announcements-actions/restore/',
            response=MockResponse(
                body={
                    'job_id': 123
                }
            ),
        )
        await monolith_cian_announcementapi_mock.add_stub(
            method='GET',
            path='/announcements-actions/get-job-status/',
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
                'status_tab': status_tab,
                'action_type': action_type
            },
        )

        # assert
        assert response.data == {
            'offers': [
                {'message': None, 'offerId': offer_id_1, 'status': 'Completed'},
                {'message': 'Need more money!', 'offerId': offer_id_2, 'status': 'Error'},
            ]
        }

    @pytest.mark.parametrize('status_tab, action_type, job_status', [
        ('notActive', 'select', 'Error'),
        ('active', 'select', 'Completed'),
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
                ($31, $32, $33, $34, $35, $36, $37, $38, $39, $40, $41, $42, $43, $44, $45)
            """,
            [
                offer_id_1, master_user, master_user, 'sale', 'flat', status_tab, [], True, False, False, 'text', '{}',
                1, now, now,
                offer_id_2, user_id, master_user, 'sale', 'flat', status_tab, [], True, False, False, 'text', '{}', 1,
                now, now,
                offer_id_3, user_id, master_user, 'sale', 'flat', status_tab, [], True, False, False, 'text', '{}', 1,
                now, now,
            ]
        )

        await monolith_cian_announcementapi_mock.add_stub(
            method='POST',
            path='/announcements-actions/restore/',
            response=MockResponse(
                body={
                    'job_id': 123
                }
            ),
        )
        await monolith_cian_announcementapi_mock.add_stub(
            method='GET',
            path='/announcements-actions/get-job-status/',
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
                'status_tab': status_tab,
                'offers_ids': [offer_id_1, offer_id_3],
                'action_type': action_type
            },
        )

        # assert
        assert response.data == {
            'offers': [
                {'message': None, 'offerId': offer_id_1, 'status': 'Completed'},
                {'message': 'Need more money!', 'offerId': offer_id_3, 'status': 'Error'},
            ]
        }
