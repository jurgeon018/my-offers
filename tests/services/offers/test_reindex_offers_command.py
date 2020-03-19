from datetime import datetime

import pytest
from cian_helpers.timezone import TIMEZONE
from cian_test_utils import future

from my_offers import enums
from my_offers.entities import Offer, ReindexOffer, ReindexOfferItem
from my_offers.services.offers._reindex_offers import reindex_offers_command


PATH = 'my_offers.services.offers._reindex_offers.'


@pytest.mark.gen_test
async def test_reindex_offers_command(mocker):
    # arrange
    get_reindex_items_mock = mocker.patch(
        f'{PATH}get_reindex_items',
        side_effect=[
            future([
                ReindexOfferItem(offer_id=11, created_at=datetime(2020, 3, 12)),
                ReindexOfferItem(offer_id=12, created_at=datetime(2020, 3, 12)),
            ]),
            future([]),
        ]
    )
    get_offers_for_reindex_mock = mocker.patch(
        f'{PATH}get_offers_for_reindex',
        return_value=future(
            [
                ReindexOffer(offer_id=11, updated_at=datetime(2020, 3, 11), raw_data='{"offerId": 11}'),
                ReindexOffer(offer_id=12, updated_at=datetime(2020, 3, 14), raw_data='{"offerId": 12}'),
            ]
        )
    )

    offer = Offer(
        offer_id=165456885,
        master_user_id=15062425,
        user_id=15062425,
        deal_type=enums.DealType.rent,
        offer_type=enums.OfferType.flat,
        status_tab=enums.OfferStatusTab.active,
        search_text='165456885 zzzzzzzzz выапывапвыапыпыпвыапывапывапыап +79994606004 +79982276978 '
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

    prepare_offer_mock = mocker.patch(
        f'{PATH}prepare_offer',
        return_value=future(offer)
    )
    update_offer_mock = mocker.patch(
        f'{PATH}update_offer',
        return_value=future()
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

    # act
    await reindex_offers_command()

    # assert
    assert get_reindex_items_mock.call_count == 2
    get_offers_for_reindex_mock.assert_called_once_with([11, 12])
    prepare_offer_mock.assert_called_once_with(object_model)
    object_model_mapper_mock.assert_called_once_with({'offerId': 11})
    update_offer_mock.assert_called_once_with(offer)
    delete_reindex_items_mock.assert_called_once_with([11, 12])
