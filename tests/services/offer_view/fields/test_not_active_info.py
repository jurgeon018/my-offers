from datetime import datetime

import pytest
import pytz
from freezegun import freeze_time

from my_offers.entities.get_offers import NotActiveInfo
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Status
from my_offers.services.offer_view.fields import get_not_active_info


@pytest.mark.parametrize(
    ('status', 'import_error', 'archive_date', 'now', 'expected'),
    (
        (None, 'zzzz', None, datetime(2020, 3, 5), NotActiveInfo(status='Ошибка импорта', message='zzzz')),
        (None, None, None, datetime(2020, 3, 5), None),
        (Status.draft, None, None, datetime(2020, 3, 5), NotActiveInfo(status='Черновик', message=None)),
        (Status.deactivated, None, None, datetime(2020, 3, 5), NotActiveInfo(status='Снято с публикации')),
        (
            Status.deactivated,
            None,
            datetime(2020, 3, 10, tzinfo=pytz.UTC),
            datetime(2020, 3, 5),
            NotActiveInfo(status='Снято с публикации', message='До автоматического удаления осталось 5 дней')
        ),
        (Status.published, None, None, datetime(2020, 3, 5), None),
    )
)
def test_get_not_active_info(mocker, status, import_error, archive_date, now, expected):
    # arrange

    # act
    with freeze_time(now):
        result = get_not_active_info(status=status, import_error=import_error, archive_date=archive_date)

    # assert
    assert result == expected
