from datetime import datetime

import pytest
import pytz

from my_offers.entities.get_offers import Moderation
from my_offers.entities.moderation import OfferOffence
from my_offers.enums import ModerationOffenceStatus
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Status
from my_offers.services.offer_view.fields.moderation import get_moderation


@pytest.mark.parametrize('status, offence, expected', [
    (None, None, None),
    (Status.removed_by_moderator, None, None),
    (Status.published, None, None),
    (
        None,
        OfferOffence(
            offence_id=555,
            offence_type=1,
            offence_text='ТЕСТ',
            offence_status=ModerationOffenceStatus.corrected,
            offer_id=777,
            created_by=888,
            created_date=datetime(2020, 1, 1, tzinfo=pytz.utc),
            row_version=0,
            updated_at=None,
            created_at=None,
        ),
        None
    ),
    (
        Status.removed_by_moderator,
        OfferOffence(
            offence_id=555,
            offence_type=1,
            offence_text='ТЕСТ',
            offence_status=ModerationOffenceStatus.corrected,
            offer_id=777,
            created_by=888,
            created_date=datetime(2020, 1, 1, tzinfo=pytz.utc),
            row_version=0,
            updated_at=None,
            created_at=None,
        ),
        None
    ),
    (
        Status.removed_by_moderator,
        OfferOffence(
            offence_id=555,
            offence_type=1,
            offence_text='ТЕСТ',
            offence_status=ModerationOffenceStatus.confirmed,
            offer_id=777,
            created_by=888,
            created_date=datetime(2020, 1, 1, tzinfo=pytz.utc),
            row_version=0,
            updated_at=None,
            created_at=None,
        ),
        Moderation(
            declined_date=datetime(2020, 1, 1, tzinfo=pytz.utc),
            reason='ТЕСТ',
            is_declined=False,
            offence_status='Удалено модератором'
        )
    ),
    (
        Status.refused,
        OfferOffence(
            offence_id=555,
            offence_type=1,
            offence_text='ТЕСТ',
            offence_status=ModerationOffenceStatus.confirmed,
            offer_id=777,
            created_by=888,
            created_date=datetime(2020, 1, 1, tzinfo=pytz.utc),
            row_version=0,
            updated_at=None,
            created_at=None,
        ),
        Moderation(
            declined_date=datetime(2020, 1, 1, tzinfo=pytz.utc),
            reason='ТЕСТ',
            is_declined=True,
            offence_status='Отклонено модератором'
        )
    ),
    (
        Status.blocked,
        OfferOffence(
            offence_id=555,
            offence_type=1,
            offence_text='ТЕСТ',
            offence_status=ModerationOffenceStatus.confirmed,
            offer_id=777,
            created_by=888,
            created_date=datetime(2020, 1, 1, tzinfo=pytz.utc),
            row_version=0,
            updated_at=None,
            created_at=None,
        ),
        Moderation(
            declined_date=None,
            is_declined=False,
            offence_status='Заблокировано'
        )
    ),
])
def test_get_status(mocker, status, offence, expected):
    # arrange & act
    result = get_moderation(status=status, offer_offence=offence)

    # assert
    assert result == expected
