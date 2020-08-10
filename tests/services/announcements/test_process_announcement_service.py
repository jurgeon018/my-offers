import pytest
from cian_test_utils import future

from my_offers.services.announcement.process_announcement_service import (
    AnnouncementProcessor,
    ForceAnnouncementProcessor,
)


async def test_force_announcement_processor_save(mocker):
    # arrange
    processor = ForceAnnouncementProcessor()
    offer = mocker.sentinel.offer
    update_offer_mock = mocker.patch(
        'my_offers.services.announcement.process_announcement_service.update_offer',
        return_value=future()
    )

    # act
    await processor._save_offer(offer)

    # assert
    update_offer_mock.assert_called_once_with(offer)


async def test_announcement_processor(mocker):
    # arrange
    processor = AnnouncementProcessor()
    offer = mocker.sentinel.offer

    # act & assert
    with pytest.raises(NotImplementedError):
        await processor._save_offer(offer)
