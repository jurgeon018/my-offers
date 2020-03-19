from datetime import datetime

import pytest
import pytz
from cian_test_utils import future, v

from freezegun import freeze_time
from my_offers.entities import ModerationOfferOffence
from my_offers.entities.moderation import OfferOffence
from my_offers.enums import ModerationOffenceStatus
from my_offers.services.moderation.moderation_service import save_offer_offence


pytestmark = pytest.mark.gen_test


async def test_save_offer_offence(mocker):
    # arrange
    now = datetime.now(pytz.utc)
    moderation_offer_offence = v(ModerationOfferOffence(
        offence_id=555,
        offence_type=1,
        text_for_user='ТЕСТ',
        state=ModerationOffenceStatus.confirmed,
        object_id=777,
        created_by=888,
        created_date=datetime(2020, 1, 1),
        date=datetime(2020, 1, 1),
        row_version=0,
        operation_id='1233123213123231',
    ))
    offer_offence = OfferOffence(
        offence_id=555,
        offence_type=1,
        offence_text='ТЕСТ',
        offence_status=ModerationOffenceStatus.confirmed,
        offer_id=777,
        created_by=888,
        created_date=datetime(2020, 1, 1),
        row_version=0,
        updated_at=now,
        created_at=now,
    )
    save_offer_contract_mock = mocker.patch(
        'my_offers.services.moderation.moderation_service.postgresql.save_offer_offence',
        return_value=future()
    )

    # act
    with freeze_time(now):
        await save_offer_offence(offer_offence=moderation_offer_offence)

    # assert
    save_offer_contract_mock.assert_called_with(offer_offence=offer_offence)


async def test_save_offer_offence__row_version_is_none(mocker):
    # arrange
    now = datetime.now(pytz.utc)
    moderation_offer_offence = v(ModerationOfferOffence(
        offence_id=555,
        offence_type=1,
        text_for_user='ТЕСТ',
        state=ModerationOffenceStatus.confirmed,
        object_id=777,
        created_by=888,
        created_date=datetime(2020, 1, 1),
        date=datetime(2020, 1, 1),
        row_version=None,
        operation_id='1233123213123231',
    ))
    offer_offence = OfferOffence(
        offence_id=555,
        offence_type=1,
        offence_text='ТЕСТ',
        offence_status=ModerationOffenceStatus.confirmed,
        offer_id=777,
        created_by=888,
        created_date=datetime(2020, 1, 1),
        row_version=0,
        updated_at=now,
        created_at=now,
    )
    save_offer_contract_mock = mocker.patch(
        'my_offers.services.moderation.moderation_service.postgresql.save_offer_offence',
        return_value=future()
    )

    # act
    with freeze_time(now):
        await save_offer_offence(offer_offence=moderation_offer_offence)

    # assert
    save_offer_contract_mock.assert_called_with(offer_offence=offer_offence)
