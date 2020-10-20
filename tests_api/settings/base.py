import uuid

from cian_automation.settings.base import *  # pylint: disable=wildcard-import,unused-wildcard-import

from my_offers.settings.base import *


X_PASS_KEY = '87C8573A-BD08-4A54-BF33-DBBD2AF78551'
HEADERS = {
    'X-PassKey': X_PASS_KEY,
    'X-TestMode': '1',
    'X-Real-Email': '',
    'X-Authenticated': '1',
    'X-EnableTwoFactor': 'false',
}

HEADERS_ON_TEST = {
    'X-OperationId': lambda: str(uuid.uuid4()),
}

PATH_TO_SERVICES = 'tests_api.cian.services'
