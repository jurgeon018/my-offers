from datetime import datetime

from cian_helpers.timezone import TIMEZONE
from cian_test_utils import future
from simple_settings.utils import settings_stub

from my_offers import enums
from my_offers.entities import Offer, ReindexOffer, ReindexOfferItem
from my_offers.repositories.monolith_cian_elasticapi.entities import (
    ElasticResultIElasticAnnouncementElasticAnnouncementError,
)
from my_offers.services.announcement.process_announcement_service import ForceAnnouncementProcessor
from my_offers.services.offers._reindex_offers import get_offers_from_elasticapi_for_reindex, reindex_offers_command


PATH = 'my_offers.services.offers._reindex_offers.'


async def test_reindex_offers_command(mocker):
    # arrange
    get_reindex_items_mock = mocker.patch(
        f'{PATH}get_reindex_items',
        side_effect=[
            future([
                ReindexOfferItem(offer_id=11, created_at=datetime(2020, 3, 12), sync=True),
                ReindexOfferItem(offer_id=12, created_at=datetime(2020, 3, 12)),
            ]),
            future([]),
        ]
    )
    get_offers_from_elasticapi_for_reindex_mock = mocker.patch(
        f'{PATH}get_offers_from_elasticapi_for_reindex',
        return_value=future([
            ReindexOffer(offer_id=11, updated_at=datetime(2020, 3, 11), raw_data='{"offerId": 11}'),
        ])
    )
    get_offers_for_reindex_mock = mocker.patch(
        f'{PATH}get_offers_for_reindex',
        return_value=future([
            ReindexOffer(offer_id=12, updated_at=datetime(2020, 3, 11), raw_data='{"offerId": 12}'),
        ])
    )
    delete_reindex_items_mock = mocker.patch(
        f'{PATH}delete_reindex_items',
        return_value=future()
    )

    object_model = mocker.sentinel.offer_model
    object_model_mapper_mock = mocker.patch(
        f'{PATH}object_model_mapper.map_from',
        return_value=object_model
    )

    process_mock = mocker.patch.object(
        ForceAnnouncementProcessor,
        'process',
        return_value=future(),
    )

    # act
    await reindex_offers_command()

    # assert
    assert get_reindex_items_mock.call_count == 2
    get_offers_for_reindex_mock.assert_called_once_with([12])
    get_offers_from_elasticapi_for_reindex_mock.assert_called_once_with([11])
    object_model_mapper_mock.assert_has_calls([
        mocker.call({'offerId': 12}),
        mocker.call({'offerId': 11}),
    ])
    assert process_mock.call_count == 2
    delete_reindex_items_mock.assert_called_once_with([11, 12])


async def test_get_offers_from_elasticapi_for_reindex(mocker):
    # arrange
    get_api_elastic_announcement_get_mock = mocker.patch(
        f'{PATH}get_api_elastic_announcement_get',
        return_value=future(ElasticResultIElasticAnnouncementElasticAnnouncementError(success=[mocker.sentinel]))
    )

    # act
    with settings_stub(ELASTIC_API_BULK_SIZE=1):
        result = await get_offers_from_elasticapi_for_reindex([11, 12])

    # assert
    assert get_api_elastic_announcement_get_mock.call_count == 2
    assert result == [
        ReindexOffer(offer_id=mocker.sentinel.realty_object_id, raw_data=mocker.sentinel.object_model, updated_at=None),
        ReindexOffer(offer_id=mocker.sentinel.realty_object_id, raw_data=mocker.sentinel.object_model, updated_at=None)
    ]
