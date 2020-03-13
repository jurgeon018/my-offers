from datetime import datetime

import pytest
from freezegun import freeze_time
from simple_settings.utils import settings_stub

from my_offers.entities.get_offers import NotActiveInfo
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Status
from my_offers.services.offer_view.fields import get_not_active_info


TODAY = datetime(2020, 3, 12, 5)
EDIT_DAY = datetime(2020, 3, 10, 10)
CHECK_STR = '28 дней'

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
            datetime(2019, 3, 10, 10),
            TODAY,
            NotActiveInfo(status='Снято с публикации', message=None)
        ),
        (
            Status.deactivated,
            None,
            EDIT_DAY,
            TODAY,
            NotActiveInfo(status='Снято с публикации', message=f'До автоматического удаления осталось {CHECK_STR}')
        ),
        (
            Status.deleted,
            None,
            EDIT_DAY,
            TODAY,
            NotActiveInfo(status='Снято с публикации', message=f'До автоматического удаления осталось {CHECK_STR}')
        ),
        (
            Status.removed_by_moderator,
            None,
            EDIT_DAY,
            TODAY,
            NotActiveInfo(status='Снято с публикации', message=f'До автоматического удаления осталось {CHECK_STR}')
        ),
        (
            Status.refused,
            None,
            EDIT_DAY,
            TODAY,
            NotActiveInfo(status='Снято с публикации', message=f'До автоматического удаления осталось {CHECK_STR}')
        ),
        (
            Status.sold,
            None,
            EDIT_DAY,
            TODAY,
            NotActiveInfo(status='Снято с публикации', message=f'До автоматического удаления осталось {CHECK_STR}')
        ),
        (
            Status.moderate,
            None,
            EDIT_DAY,
            TODAY,
            NotActiveInfo(status='Снято с публикации', message=f'До автоматического удаления осталось {CHECK_STR}')
        ),
        (
            Status.blocked,
            None,
            EDIT_DAY,
            TODAY,
            NotActiveInfo(status='Снято с публикации', message=f'До автоматического удаления осталось {CHECK_STR}')
        ),
    )
)
def test_get_not_active_info(mocker, status, import_error, edit_date, now, expected):
    # arrange

    # act
    with settings_stub(DAYS_BEFORE_ARCHIVATION=30):
        with freeze_time(now):
            result = get_not_active_info(
                status=status,
                import_error=import_error,
                edit_date=edit_date
            )

    # assert
    assert result == expected
