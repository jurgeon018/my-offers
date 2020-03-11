from datetime import datetime

from my_offers.entities.get_offers import DeclinedInfo
from my_offers.entities.moderation import OfferOffence
from my_offers.enums import ModerationOffenceStatus
from my_offers.services.offer_view.fields.declined_info import get_declined_info
from tests_api.cian.announcementapi.entities.object_model import Status


def test_get_declined_info(mocker):
    # arrange
    status = Status.blocked
    offer_offence = OfferOffence(
        offence_id=555,
        offence_type=1,
        offence_text='ТЕСТ',
        offence_status=ModerationOffenceStatus.confirmed,
        offer_id=777,
        created_by=888,
        created_date=datetime(2020, 1, 1),
        row_version=0,
        updated_at=datetime(2020, 1, 1),
        created_at=datetime(2020, 1, 1),
    )

    expected = DeclinedInfo(moderation=None)

    # act
    result = get_declined_info(status=status, offer_offence=offer_offence)

    # assert
    assert result == expected
