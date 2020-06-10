from datetime import datetime

import pytest
import pytz
from freezegun import freeze_time

from my_offers.entities.get_offers import NotActiveInfo
from my_offers.enums.not_active_status import NotActiveStatus
from my_offers.repositories.monolith_cian_announcementapi.entities.object_model import Status
from my_offers.services.offer_view.fields import get_not_active_info


@freeze_time('2020-03-01 5:00')
@pytest.mark.parametrize(
    ('status', 'import_error', 'archive_date', 'expected'),
    (
        (None, 'zzzz', None, NotActiveInfo(
            status='Ошибка импорта',
            message='zzzz',
            status_type=NotActiveStatus.import_error)
         ),
        (None, None, None, None),
        (Status.draft, None, None, NotActiveInfo(
            status='Черновик',
            message=None,
            status_type=NotActiveStatus.discontinued)
         ),
        (Status.deactivated, None, None, NotActiveInfo(
            status='Снято с публикации',
            status_type=NotActiveStatus.discontinued
        )),
        (Status.published, None, None, None),
        (
            Status.deactivated,
            None,
            datetime(2019, 3, 31, 5, tzinfo=pytz.UTC),
            NotActiveInfo(status='Снято с публикации', message=None, status_type=NotActiveStatus.discontinued)
        ),
        (
            Status.deactivated,
            None,
            datetime(2020, 3, 10, 10, tzinfo=pytz.UTC),
            NotActiveInfo(
                status='Снято с публикации',
                message='Будет автоматически перенесено в архив через 9 дней',
                status_type=NotActiveStatus.discontinued
            )
        ),
        (
            Status.deleted,
            None,
            datetime(2020, 3, 10, 10, tzinfo=pytz.UTC),
            NotActiveInfo(
                status='Снято с публикации',
                message='Будет автоматически перенесено в архив через 9 дней',
                status_type=NotActiveStatus.discontinued
            )
        ),
        (
            Status.removed_by_moderator,
            None,
            datetime(2020, 3, 10, 10, tzinfo=pytz.UTC),
            NotActiveInfo(
                status='Снято с публикации',
                message='Будет автоматически перенесено в архив через 9 дней',
                status_type=NotActiveStatus.discontinued
            )
        ),
        (
            Status.refused,
            None,
            datetime(2020, 3, 10, 10, tzinfo=pytz.UTC),
            NotActiveInfo(
                status='Снято с публикации',
                message='Будет автоматически перенесено в архив через 9 дней',
                status_type=NotActiveStatus.discontinued
            )
        ),
        (
            Status.sold,
            None,
            datetime(2020, 3, 10, 10, tzinfo=pytz.UTC),
            NotActiveInfo(
                status='Снято с публикации',
                message='Будет автоматически перенесено в архив через 9 дней',
                status_type=NotActiveStatus.discontinued
            )
        ),
        (
            Status.moderate,
            None,
            datetime(2020, 3, 10, 10, tzinfo=pytz.UTC),
            NotActiveInfo(
                status='Снято с публикации',
                message='Будет автоматически перенесено в архив через 9 дней',
                status_type=NotActiveStatus.discontinued
            )
        ),
        (
            Status.blocked,
            None,
            datetime(2020, 3, 10, 10, tzinfo=pytz.UTC),
            NotActiveInfo(
                status='Снято с публикации',
                message='Будет автоматически перенесено в архив через 9 дней',
                status_type=NotActiveStatus.discontinued
            )
        ),
    )
)
def test_get_not_active_info(status, import_error, archive_date, expected):
    # arrange

    # act
    result = get_not_active_info(
        status=status,
        import_error=import_error,
        archive_date=archive_date
    )

    # assert
    assert result == expected


def test_get_not_active_info__premoderation__premoderation():
    # arrange
    expected = NotActiveInfo(
        status='На модерации',
        message='Объявление будет автоматически опубликовано после проверки модератором',
        status_type=NotActiveStatus.premoderation
    )

    # act
    result = get_not_active_info(status=None, on_premoderation=True)

    # assert
    assert result == expected
