from datetime import datetime

from cian_functional_test_utils.pytest_plugin import MockResponse


class TestChangeOffersPublisher:

    async def test_change_offers_publisher(
            self,
            pg,
            http,
            monolith_cian_announcementapi_mock
    ):
        """ Проверяем флоу смены владельца объявления """
        # arrange
        offer_id_1 = 11111111
        offer_id_2 = 22222222
        user_id = 222
        master_user = 333
        status_tab = 'notActive'
        job_state = 'Error'

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
            path='/announcements-actions/v1/change-owner/',
            body={
                'actorId': master_user,
                'announcementIds': [offer_id_2],
                'newOwnerId': user_id
            },
            response=MockResponse(
                body={
                    'job_id': 123,
                    'is_new': False
                }
            ),
        )
        await monolith_cian_announcementapi_mock.add_stub(
            method='GET',
            path='/announcements-actions/v1/get-job-status/',
            query={
                'JobId': 123
            },
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
                        'state': job_state,
                        'announcementsProgress': [
                            {'id': offer_id_2, 'state': 'Error', 'error_message': 'Need more money!'},
                        ]
                    }
                ),
            ]
        )

        # act
        response = await http.request(
            'POST',
            '/public/v1/actions/change-offers-publisher/',
            headers={
                'X-Real-UserId': master_user
            },
            json={
                'user_id': user_id,
                'offers_ids': [offer_id_2]
            },
        )

        # assert
        assert response.data == {
            'offers': [
                {'message': 'Need more money!', 'offerId': offer_id_2, 'status': 'Error'},
            ]
        }

    async def test_change_offers_publisher__offers_ids_is_empty(self, pg, http):
        """ При пустом offers_ids возвращаем пустой результат """
        # arrange
        master_user = 333
        user_id = 222

        # act
        response = await http.request(
            'POST',
            '/public/v1/actions/change-offers-publisher/',
            headers={
                'X-Real-UserId': master_user
            },
            json={
                'user_id': user_id,
                'offers_ids': []
            },
        )

        # assert
        assert response.data == {'offers': []}

    async def test_change_offers_publisher__external_api_raise_bad_request_exc(
            self,
            pg,
            http,
            monolith_cian_announcementapi_mock
    ):
        """ Проверяем прокидываение 400 из ответов внешних апи """
        # arrange
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

        await monolith_cian_announcementapi_mock.add_stub(
            method='POST',
            path='/announcements-actions/v1/change-owner/',
            body={
                'actorId': master_user,
                'announcementIds': [offer_id_2],
                'newOwnerId': user_id
            },
            response=MockResponse(
                status=400,
                body={
                    'errors': [{
                        'code': 'wrong_type',
                        'key': 'user_id',
                        'message': 'User id send with wrong type',
                    }]
                }
            ),
        )

        # act
        response = await http.request(
            'POST',
            '/public/v1/actions/change-offers-publisher/',
            headers={
                'X-Real-UserId': master_user
            },
            json={
                'user_id': user_id,
                'offers_ids': [offer_id_2]
            },
            expected_status=400
        )

        # assert
        assert response.data == {
            'errors': [{
                'code': 'wrongType',
                'key': 'userId',
                'message': 'User id send with wrong type'
            }],
            'message': 'User id send with wrong type'
        }

    async def test_change_offers_publisher__get_job_status_return_error(
            self,
            pg,
            http,
            monolith_cian_announcementapi_mock
    ):
        """ Апи статуса джобы возвращает 500 """
        # arrange
        offer_id_1 = 11111111
        offer_id_2 = 22222222
        user_id = 222
        master_user = 333
        status_tab = 'notActive'
        job_state = 'Error'

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
            path='/announcements-actions/v1/change-owner/',
            body={
                'actorId': master_user,
                'announcementIds': [offer_id_2],
                'newOwnerId': user_id
            },
            response=MockResponse(
                body={
                    'job_id': 123,
                    'is_new': False
                }
            ),
        )
        await monolith_cian_announcementapi_mock.add_stub(
            method='GET',
            path='/announcements-actions/v1/get-job-status/',
            query={
                'JobId': 123
            },
            response=[
                MockResponse(
                    status=500,
                    repeat=3
                ),
                MockResponse(
                    body={
                        'state': job_state,
                        'announcementsProgress': [
                            {'id': offer_id_2, 'state': 'Error', 'error_message': 'Need more money!'},
                        ]
                    }
                ),
            ]
        )

        # act
        response = await http.request(
            'POST',
            '/public/v1/actions/change-offers-publisher/',
            headers={
                'X-Real-UserId': master_user
            },
            json={
                'user_id': user_id,
                'offers_ids': [offer_id_2]
            },
        )

        # assert
        assert response.data == {
            'offers': [
                {'message': 'Need more money!', 'offerId': offer_id_2, 'status': 'Error'},
            ]
        }
