import random
from datetime import datetime, timedelta

import pytest
import pytz
from freezegun import freeze_time
from simple_settings import settings

from my_offers.entities.get_offers import NotActiveInfo
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Status
from my_offers.services.offer_view.fields import get_not_active_info
from my_offers.services.offer_view.helpers.time import get_left_time_display


TODAY = datetime(2020, 3, 12)
EDIT_DAY = datetime(2020, 3, 10)
ARCHIVE_DAY = EDIT_DAY + timedelta(days=settings.DAYS_BEFORE_ARCHIVATION)
CHECK_DAYS = get_left_time_display(current=TODAY, end=ARCHIVE_DAY)

@pytest.mark.parametrize(
    ('status', 'import_error', 'edit_date', 'now', 'expected'),
    (
        (None, 'zzzz', None, TODAY, NotActiveInfo(status='Ошибка импорта', message='zzzz')),
        (None, None, None, TODAY, None),
        (Status.draft, None, None, TODAY, NotActiveInfo(status='Черновик', message=None)),
        (Status.deactivated, None, None, TODAY, NotActiveInfo(status='Снято с публикации')),
        (Status.published, None, None, TODAY, None),
        (
            Status.deactivated,
            None,
            EDIT_DAY - timedelta(days=settings.DAYS_BEFORE_ARCHIVATION),
            TODAY,
            NotActiveInfo(status='Снято с публикации', message=None)
        ),
        (
            Status.deactivated,
            None,
            EDIT_DAY,
            TODAY,
            NotActiveInfo(status='Снято с публикации', message=f'До автоматического удаления осталось {CHECK_DAYS}')
        ),
        (
            Status.deleted,
            None,
            EDIT_DAY,
            TODAY,
            NotActiveInfo(status='Снято с публикации', message=f'До автоматического удаления осталось {CHECK_DAYS}')
        ),
        (
            Status.removed_by_moderator,
            None,
            EDIT_DAY,
            TODAY,
            NotActiveInfo(status='Снято с публикации', message=f'До автоматического удаления осталось {CHECK_DAYS}')
        ),
        (
            Status.refused,
            None,
            EDIT_DAY,
            TODAY,
            NotActiveInfo(status='Снято с публикации', message=f'До автоматического удаления осталось {CHECK_DAYS}')
        ),
        (
            Status.sold,
            None,
            EDIT_DAY,
            TODAY,
            NotActiveInfo(status='Снято с публикации', message=f'До автоматического удаления осталось {CHECK_DAYS}')
        ),
        (
            Status.moderate,
            None,
            EDIT_DAY,
            TODAY,
            NotActiveInfo(status='Снято с публикации', message=f'До автоматического удаления осталось {CHECK_DAYS}')
        ),
        (
            Status.blocked,
            None,
            EDIT_DAY,
            TODAY,
            NotActiveInfo(status='Снято с публикации', message=f'До автоматического удаления осталось {CHECK_DAYS}')
        ),
    )
)
def test_get_not_active_info(mocker, status, import_error, edit_date, now, expected):
    # arrange

    # act
    with freeze_time(now):
        result = get_not_active_info(status=status, import_error=import_error, edit_date=edit_date)

    # assert
    assert result == expected
