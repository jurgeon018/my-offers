from typing import List

from cian_core.settings.base import *  # pylint: disable=wildcard-import,unused-wildcard-import


APPLICATION_NAME = 'my-offers'
APPLICATION_DESCRIPTION = 'МКС: мои объявления для агента'
APPLICATION_PACKAGE_NAME = 'my_offers'

CHECK_SERVICES: List[str] = []

DEFAULT_LOCATION_ID: int = 1

DB_TIMEOUT: float = 3

CIAN_BASE_URL: str = 'https://cian.ru'

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

RESEND_JOB_REFRESH: float = .5
RESEND_JOB_BROADCAST_TYPE: str = 'temp'
