from typing import List

from cian_core.settings.base import *  # pylint: disable=wildcard-import,unused-wildcard-import


APPLICATION_NAME = 'my-offers'
APPLICATION_DESCRIPTION = 'МКС: мои объявления для агента'
APPLICATION_PACKAGE_NAME = 'my_offers'

CHECK_SERVICES: List[str] = []


PROCESS_ANNOUNCEMENT_CONSUMER_PREFETCH_COUNT: int = 1
