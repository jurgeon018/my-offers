import pytest
from cian_test_utils import future

from my_offers.services.announcement.process_announcement_service import (
    AnnouncementProcessor,
    ForceAnnouncementProcessor,
)
from my_offers.repositories.monolith_cian_announcementapi.entities import BargainTerms, ObjectModel, Phone
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Category



async def test_force_announcement_processor_save(mocker):
    # arrange
    processor = ForceAnnouncementProcessor()
    offer = mocker.sentinel.offer
    update_offer_mock = mocker.patch(
        'my_offers.services.announcement.process_announcement_service.postgresql.update_offer',
        return_value=future()
    )

    # act
    await processor._save_offer(offer)

    # assert
    update_offer_mock.assert_called_once_with(offer)


async def test_announcement_processor_raises_on_save_offer(mocker):
    # arrange
    processor = AnnouncementProcessor()
    offer = mocker.sentinel.offer

    # act & assert
    with pytest.raises(NotImplementedError):
        await processor._save_offer(offer)


async def test_announcement_processor(mocker):
    # arrange
    offer_id = 1
    master_user_id = 1
    payed_by = 1
    object_model = ObjectModel(
        id=offer_id,
        bargain_terms=BargainTerms(price=1),
        category=Category.office_sale,
        phones=[Phone(country_code='1', number='12312')],
        user_id=222,
        total_area=100,
        can_parts=True,
        min_area=7,
    )
    offer = mocker.sentinel.offer

    get_master_user_id_mock = mocker.patch.object(
        AnnouncementProcessor,
        '_get_master_user_id',
        return_value=future(master_user_id)
    )
    get_payed_by_mock = mocker.patch(
        'my_offers.services.announcement.process_announcement_service.get_payed_by',
        return_value=future(payed_by)
    )
    prepare_offer_mock = mocker.patch.object(
        AnnouncementProcessor,
        '_prepare_offer',
        return_value=offer
    )
    save_offer_mock = mocker.patch.object(
        AnnouncementProcessor,
        '_save_offer',
        return_value=future()
    )
    post_process_offer_mock = mocker.patch.object(
        AnnouncementProcessor,
        '_post_process_offer',
        return_value=future()
    )

    processor = AnnouncementProcessor()

    # act
    await processor.process(object_model)

    # assert
    get_master_user_id_mock.assert_called_once()
    get_payed_by_mock.assert_called_once_with(offer_id=offer_id)
    prepare_offer_mock.assert_called_once_with(
         mocker.ANY,
         object_model=object_model,
         master_user_id=master_user_id,
         payed_by=payed_by)
    save_offer_mock.assert_called_once_with(mocker.ANY, offer)
    post_process_offer_mock.assert_called_once_with(mocker.ANY, object_model)
