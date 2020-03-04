import pytest
from cian_test_utils import future

from my_offers import entities
from my_offers.repositories.monolith_cian_announcementapi.entities import V1GetAnnouncement
from my_offers.services.offers import update_offer


@pytest.mark.gen_test
async def test_update_offer(mocker):
    # arrange
    object_model = mocker.sentinel.object_model
    v1_get_announcement_mock = mocker.patch(
        'my_offers.services.offers._update_offer.v1_get_announcement',
        return_value=future(object_model),
    )
    process_announcement_mock = mocker.patch(
        'my_offers.services.offers._update_offer.process_announcement',
        return_value=future(),
    )

    map_to_mock = mocker.patch(
        'my_offers.services.offers._update_offer.object_model_mapper.map_to',
        return_value={'id': 11},
    )

    # act
    await update_offer(entities.UpdateOfferRequest(offer_id=11))

    # assert
    v1_get_announcement_mock.assert_called_once_with(V1GetAnnouncement(id=11))
    process_announcement_mock.assert_called_once_with({'id': 11})
    map_to_mock.assert_called_once_with(object_model)
