from datetime import datetime

import pytest
from cian_helpers.timezone import TIMEZONE
from cian_test_utils import future

from my_offers import entities, enums
from my_offers.mappers.object_model import object_model_mapper
from my_offers.repositories.monolith_cian_announcementapi.entities import BargainTerms, ObjectModel, Phone
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category, Status
from my_offers.repositories.monolith_cian_announcementapi.entities.publish_term import Services
from my_offers.services.announcement import process_announcement
from my_offers.services.announcement.process_announcement_service import post_process_announcement
from tests.utils import load_json_data


@pytest.fixture(name='announcement')
def announcement_fixture():
    return object_model_mapper.map_from(load_json_data(__file__, 'announcement.json'))


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
        search_text='165456885 9994606004 9982276978 Россия, Ростов-на-Дону, Большая Садовая улица, 73 Ростовская '
                    'область Ростов-на-Дону Большая Садовая улица 73 д73 д 73 73д Кировский Центр район 1-комн. кв., '
                    '123 м², 1/3 этаж zzzzzzzzz 1 комн комнатная 1 3 выапывапвыапыпыпвыапывапывапыап',
        row_version=announcement.row_version,
        raw_data=object_model_mapper.map_to(announcement),
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

    # act
    await process_announcement(announcement)

    # assert
    save_offer_mock.assert_called_once_with(offer)


@pytest.mark.gen_test
async def test_post_process_announcement(mocker):
    # arrange
    offer = ObjectModel(
        id=111,
        bargain_terms=BargainTerms(price=123),
        phones=[Phone(country_code='1', number='12312')],
        category=Category.flat_rent,
        status=Status.published,
    )
    delete_offer_import_error_mock = mocker.patch(
        'my_offers.services.announcement.process_announcement_service.postgresql.delete_offer_import_error',
        return_value=future(),
    )

    # act
    await post_process_announcement(offer)

    # assert
    delete_offer_import_error_mock.assert_called_once_with(111)
