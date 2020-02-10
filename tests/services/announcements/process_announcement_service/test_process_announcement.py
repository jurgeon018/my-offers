from datetime import datetime

import pytest
from cian_helpers.timezone import TIMEZONE
from cian_test_utils import future

from my_offers import entities, enums
from my_offers.services.announcement import process_announcement
from tests.utils import load_json_data


@pytest.fixture(name='announcement')
def announcement_fixture():
    return load_json_data(__file__, 'announcement.json')


@pytest.mark.gen_test
async def test_process_announcement(mocker, announcement):
    # arrange
    save_offer_mock = mocker.patch(
        'my_offers.services.announcement.process_announcement_service.postgresql.save_offer',
        return_value=future(),
    )
    offer = entities.Offer(
        offer_id=165456885,
        master_user_id=15062425,
        user_id=15062425,
        deal_type=enums.DealType.rent,
        offer_type=enums.OfferType.flat,
        status_tab=enums.OfferStatusTab.active,
        search_text='165456885 выапывапвыапыпыпвыапывапывапыап +79994606004 +79982276978 Россия, Ростов-на-Дону, '
                    'Большая Садовая улица, 73',
        row_version=announcement['rowVersion'],
        raw_data=announcement,
        services=[enums.Services.highlight, enums.Services.calltracking, enums.Services.premium],
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

    # act
    await process_announcement(announcement)

    # assert
    save_offer_mock.assert_called_once_with(offer)
