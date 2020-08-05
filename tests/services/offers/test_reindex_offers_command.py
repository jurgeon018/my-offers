from datetime import datetime

import pytest
from cian_helpers.timezone import TIMEZONE
from cian_test_utils import future
from simple_settings.utils import settings_stub

from my_offers import enums
from my_offers.entities import Offer, ReindexOffer, ReindexOfferItem
from my_offers.repositories.monolith_cian_elasticapi.entities import (
    ElasticResultIElasticAnnouncementElasticAnnouncementError,
)
from my_offers.services.offers._reindex_offers import get_offers_from_elasticapi_for_reindex, reindex_offers_command


PATH = 'my_offers.services.offers._reindex_offers.'


@pytest.mark.skip
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

    offer = Offer(
        offer_id=165456885,
        master_user_id=15062425,
        user_id=15062425,
        deal_type=enums.DealType.rent,
        offer_type=enums.OfferType.flat,
        status_tab=enums.OfferStatusTab.active,
        search_text='165456885 zzzzzzzzz выапывапвыапыпыпвыапывапывапыап 9994606004 9982276978 '
                    'Россия, Ростов-на-Дону, Большая Садовая улица, 73',
        row_version=222,
        raw_data={'offerId': 11},
        services=[enums.OfferServices.premium, enums.OfferServices.premium_highlight],
        is_manual=True,
        is_in_hidden_base=False,
        has_photo=False,
        is_test=True,
        price=12332.0,
        price_per_meter=100.26,
        total_area=123.0,
        walking_time=None,
        street_name='Большая Садовая',
        sort_date=TIMEZONE.localize(datetime(2020, 2, 7, 16, 25, 37, 99015)),
    )

    # prepare_offer_mock = mocker.patch(
    #     f'{PATH}prepare_offer',
    #     return_value=future(offer)
    # )
    # update_offer_mock = mocker.patch(
    #     f'{PATH}update_offer',
    #     return_value=future()
    # )
    delete_reindex_items_mock = mocker.patch(
        f'{PATH}delete_reindex_items',
        return_value=future()
    )

    object_model = mocker.sentinel.offer_model
    object_model.id = 1
    object_model_mapper_mock = mocker.patch(
        f'{PATH}object_model_mapper.map_from',
        return_value=object_model
    )

    # act
    await reindex_offers_command()

    # assert
    assert get_reindex_items_mock.call_count == 2
    get_offers_for_reindex_mock.assert_called_once_with([12])
    get_offers_from_elasticapi_for_reindex_mock.assert_called_once_with([11])
    # assert prepare_offer_mock.call_count == 2
    object_model_mapper_mock.assert_has_calls([
        mocker.call({'offerId': 12}),
        mocker.call({'offerId': 11}),
    ])
    # assert update_offer_mock.call_count == 2
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
