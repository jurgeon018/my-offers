import os

from tests_functional.utils import load_data


async def test_v2_get_offers_public__offer_not_found__400(http_client):
    # act
    response = await http_client.request(
        'POST',
        '/public/v1/get-offer-duplicates/',
        json={'offerId': 165491301, 'type': 'all'},
        headers={'X-Real-UserId': 1111},
        expected_status=400,
    )

    # assert
    assert response.data['errors'][0]['code'] == 'notFound'


async def test_v2_get_offers_public__duplicates_not_found__200(http_client, pg):
    # arrange
    await pg.execute(load_data(os.path.dirname(__file__) + '/../../', 'offers.sql'))

    # act
    response = await http_client.request(
        'POST',
        '/public/v1/get-offer-duplicates/',
        json={'offerId': 231655140, 'type': 'all'},
        headers={'X-Real-UserId': 47135244},
    )

    # assert
    assert len(response.data['offers']) == 0
