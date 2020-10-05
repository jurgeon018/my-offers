from typing import List

from cian_core.settings.base import *  # pylint: disable=wildcard-import,unused-wildcard-import


APPLICATION_NAME = 'my-offers'
APPLICATION_DESCRIPTION = 'МКС: мои объявления для агента'
APPLICATION_PACKAGE_NAME = 'my_offers'

CHECK_SERVICES: List[str] = []

DEFAULT_LOCATION_ID: int = 1

DB_TIMEOUT: float = 3

CIAN_BASE_URL: str = 'https://cian.ru'
MY_CIAN_BASE_URL: str = 'https://my.cian.ru'

OFFER_LIST_LIMIT: int = 20

DAYS_BEFORE_ARCHIVATION: int = 30
DAYS_FOR_COVERAGE: int = 10
DAYS_FOR_STATISTICS: int = 10

COUNT_DAYS_HOLD_DELETED_OFFERS: int = 7
COUNT_OFFERS_DELETE_IN_ONE_TIME: int = 100
TIMEOUT_BETWEEN_DELETE_OFFERS: int = 10 * 60

LOG_SEARCH_QUERIES: bool = True

CASSANDRA_DEFAULT_TIMEOUT: float = 1.0

SEND_PUSH_ON_NEW_DUPLICATE: bool = False  # пока не раскатили приложения пуши рассылать не надо

# mass operations
MASS_OFFERS_RESTORE_DELAY: float = .5
MASS_OFFERS_LIMIT: int = 300
MASS_OFFERS_CHANGE_OWNERS_DELAY: float = .5

# sync offers
SYNC_OFFERS_ROW_VERSION_OFFSET: int = 1000
SYNC_OFFERS_GET_DIFF_DELAY: float = .5
SYNC_OFFERS_GET_DIFF_BULK_SIZE: float = 100
SYNC_OFFERS_ALLOW_RUN_TASK: bool = False
SYNC_OFFERS_TOP_CHANGED_CNT: int = 1_000_000

ELASTIC_API_BULK_SIZE: int = 50
ELASTIC_API_DELAY: float = .05

RESEND_JOB_REFRESH: float = .5
RESEND_JOB_DELAY: float = 1.0
RESEND_JOB_BROADCAST_TYPE: str = 'temp'
RESEND_JOB_ALLOW_ELASTIC: bool = False
RESEND_TASK_BULK_SIZE: int = 5000

CURRENCIES_TTL: int = 60 * 60  # 1 day

# similar offers
DUPLICATE_CHECK_ENABLED: bool = False
SYNC_OFFER_DUPLICATES_TIMEOUT = 10
SIMILAR_PRICE_KF: float = 0.2
SIMILAR_ROOM_DELTA: int = 1

MAX_SIMILAR_FOR_DESKTOP: int = 100

# notifications
EMAIL_DUPLICATE_TEMPLATE: str = 'DoubleObject'
EMAIL_UNSUBSCRIBE_URL: str = f'{MY_CIAN_BASE_URL}/settings/duplicates'
EMAIL_USER_ALREADY_SUBSCRIBED_MSG: str = (
    'Для данного email уже есть активная подписка на уведомления о новых дублях к объектам.'
)
EMAIL_USER_NOT_SUBSCRIBED_MSG: str = (
    'Для данного email нет активной подписки на уведомления о новых дублях к объектам.'
)
EMAIL_VALIDATION_ERROR_MSG: str = 'Некорректный email.'

# reindex offers master_user_id and payed_by
REINDEX_CHUNK = 1000
REINDEX_TIMEOUT = 0.5  # секунды
