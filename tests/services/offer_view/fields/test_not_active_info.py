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


TODAY = datetime(2020, 3, 11)
DELTA_DAYS = random.choice(list(i for i in range(1, settings.DAYS_BEFORE_ARCHIVATION)))
SOME_DAY_BEFORE_TODAY = TODAY - timedelta(days=DELTA_DAYS)
ARCHIVE_DAY = SOME_DAY_BEFORE_TODAY + timedelta(days=settings.DAYS_BEFORE_ARCHIVATION)

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
            SOME_DAY_BEFORE_TODAY - timedelta(days=settings.DAYS_BEFORE_ARCHIVATION),
            TODAY,
            NotActiveInfo(status='Снято с публикации',
                          message=None)
        ),
        (
            Status.deactivated,
            None,
            SOME_DAY_BEFORE_TODAY,
            TODAY,
            NotActiveInfo(status='Снято с публикации',
                          message='До автоматического удаления осталось {}'.format(
                              get_left_time_display(current=TODAY, end=ARCHIVE_DAY)
                          ))
        ),
        (
            Status.deleted,
            None,
            SOME_DAY_BEFORE_TODAY,
            TODAY,
            NotActiveInfo(status='Снято с публикации',
                          message='До автоматического удаления осталось {}'.format(
                              get_left_time_display(current=TODAY, end=ARCHIVE_DAY)
                          ))
        ),
        (
            Status.removed_by_moderator,
            None,
            SOME_DAY_BEFORE_TODAY,
            TODAY,
            NotActiveInfo(status='Снято с публикации',
                          message='До автоматического удаления осталось {}'.format(
                              get_left_time_display(current=TODAY, end=ARCHIVE_DAY)
                          ))
        ),
        (
            Status.refused,
            None,
            SOME_DAY_BEFORE_TODAY,
            TODAY,
            NotActiveInfo(status='Снято с публикации',
                          message='До автоматического удаления осталось {}'.format(
                              get_left_time_display(current=TODAY, end=ARCHIVE_DAY)
                          ))
        ),
        (
            Status.sold,
            None,
            SOME_DAY_BEFORE_TODAY,
            TODAY,
            NotActiveInfo(status='Снято с публикации',
                          message='До автоматического удаления осталось {}'.format(
                              get_left_time_display(current=TODAY, end=ARCHIVE_DAY)
                          ))
        ),
        (
            Status.moderate,
            None,
            SOME_DAY_BEFORE_TODAY,
            TODAY,
            NotActiveInfo(status='Снято с публикации',
                          message='До автоматического удаления осталось {}'.format(
                              get_left_time_display(current=TODAY, end=ARCHIVE_DAY)
                          ))
        ),
        (
            Status.blocked,
            None,
            SOME_DAY_BEFORE_TODAY,
            TODAY,
            NotActiveInfo(status='Снято с публикации',
                          message='До автоматического удаления осталось {}'.format(
                              get_left_time_display(current=TODAY, end=ARCHIVE_DAY)
                          ))
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
