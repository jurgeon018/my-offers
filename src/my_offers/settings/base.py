from typing import List

from cian_core.settings.base import *  # pylint: disable=wildcard-import,unused-wildcard-import


APPLICATION_NAME = 'my-offers'
APPLICATION_DESCRIPTION = 'МКС: мои объявления для агента'
APPLICATION_PACKAGE_NAME = 'my_offers'

CHECK_SERVICES: List[str] = []

DEFAULT_LOCATION_ID: int = 1

CiAN_BASE_URL: str = 'https://cian.ru'

OFFER_LIST_LIMIT: int = 20

DAYS_BEFORE_ARCHIVATION: int = 30
DAYS_FOR_COVERAGE: int = 10
