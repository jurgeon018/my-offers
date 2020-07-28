import pytest
from cian_test_utils import future

from my_offers import entities
from my_offers.repositories.monolith_cian_elasticapi.entities import (
    ElasticResultIElasticAnnouncementElasticAnnouncementError,
    GetApiElasticAnnouncementGet,
    IElasticAnnouncement,
)
from my_offers.services.offers import update_offer


@pytest.mark.gen_test
async def test_update_offer(mocker):
    # arrange
    object_model = mocker.sentinel.object_model
    get_api_elastic_announcement_get_mock = mocker.patch(
        'my_offers.services.offers._update_offer.get_api_elastic_announcement_get',
        return_value=future(ElasticResultIElasticAnnouncementElasticAnnouncementError(
            success=[IElasticAnnouncement(object_model='{}')]
        )),
    )
    process_announcement_mock = mocker.patch(
        'my_offers.services.offers._update_offer.process_announcement',
        return_value=future(),
    )
    mocker.patch(
        'my_offers.services.offers._update_offer.object_model_mapper.map_from',
        return_value=object_model,
    )

    # act
    await update_offer(entities.UpdateOfferRequest(offer_id=11))

    # assert
    get_api_elastic_announcement_get_mock.assert_called_once_with(GetApiElasticAnnouncementGet(ids=[11]))
    process_announcement_mock.assert_called_once_with(object_model=object_model, event_date=mocker.ANY)
